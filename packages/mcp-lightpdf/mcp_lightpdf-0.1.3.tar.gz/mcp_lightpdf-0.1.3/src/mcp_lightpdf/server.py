from dotenv import load_dotenv
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.models import InitializationOptions
import mcp.types as types
import httpx
import os
import json
import asyncio

# 加载环境变量
load_dotenv()

# 创建Server实例
app = Server(
    name="lightpdf_convert_document",
    instructions="PDF文档转换工具，支持将PDF转换为DOCX或PNG格式。",
)

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="将PDF文档转换为其他格式，如DOCX或PNG。支持单个或多个本地文件路径或网络URL。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "oneOf": [
                            {
                                "type": "string",
                                "description": "单个要转换的PDF文件路径(绝对路径)或网络URL"
                            },
                            {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "多个要转换的PDF文件路径(绝对路径)或网络URL列表"
                            }
                        ],
                        "description": "要转换的PDF文件路径(绝对路径)或网络URL，可以是单个路径或URL列表"
                    },
                    "format": {
                        "type": "string",
                        "description": "目标格式，支持docx、png",
                        "enum": ["docx", "png"]
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "输出目录路径（可选，默认为与输入文件相同的目录或当前目录）"
                    }
                },
                "required": ["file_paths", "format"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "convert_document":
        file_paths = arguments.get("file_paths", "")
        format = arguments.get("format", "")
        output_dir = arguments.get("output_dir", "")
        return await batch_convert_documents(file_paths, format, output_dir)
    
    raise ValueError(f"未知工具: {name}")

async def batch_convert_documents(file_paths, format: str, output_dir: str = "") -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """批量转换多个PDF文件"""
    result_info = []
    context = app.request_context
    
    async def log(level: str, message: str, add_to_result: bool = True):
        """记录日志并可选择添加到结果信息中"""
        print(f"log: {message}")
        log_message = types.LoggingMessageNotification(
            method="notifications/message",
            params=types.LoggingMessageNotificationParams(
                level=getattr(types.LoggingLevel, level.lower(), "info"),
                data=message
            )
        )
        await context.session.send_notification(log_message)
        if add_to_result:
            result_info.append(message)
    
    # 处理输入参数：确保file_paths是列表
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    # 验证有效的文件路径
    if not file_paths:
        raise ValueError("未提供文件路径或URL。请指定file_paths参数。")
    
    if not format:
        raise ValueError("未指定目标格式。请使用format参数指定转换格式（docx或png）。")
    
    # 记录任务总数
    total_files = len(file_paths)
    await log("info", f"开始批量转换 {total_files} 个文件为 {format} 格式")
    
    # 存储成功和失败的结果
    success_results = []
    failed_results = []
    
    # 并发处理文件，限制并发数为3
    from asyncio import Semaphore
    semaphore = Semaphore(3)  # 最多同时处理3个文件
    
    async def process_single_file(file_index, file_path):
        """处理单个文件的转换"""
        progress_token = f"file_{file_index}"
        
        async def report_progress(progress_value, total_value, message=""):
            """报告单个文件的进度"""
            progress_notification = types.ProgressNotification(
                method="notifications/progress",
                params=types.ProgressNotificationParams(
                    progressToken=progress_token,
                    progress=float(progress_value),
                    total=float(total_value),
                    message=message
                )
            )
            await context.session.send_notification(progress_notification)
        
        try:
            # 获取信号量限制并发
            async with semaphore:
                await log("info", f"[{file_index+1}/{total_files}] 处理: {file_path}")
                await report_progress(0, 100, f"开始处理 {file_path}")
                
                # 调用单文件转换函数
                result = await convert_document(file_path, format, output_dir)
                
                # 从结果中提取摘要信息（最后一个TextContent的text字段）
                if result and len(result) > 1 and hasattr(result[-1], 'text'):
                    summary = result[-1].text
                else:
                    summary = f"[成功] 文件 {file_path} 已转换为 {format} 格式"
                
                # 添加到成功结果
                success_results.append({
                    "file_path": file_path,
                    "summary": summary
                })
                
                await report_progress(100, 100, f"完成 {file_path}")
                return True
        except Exception as e:
            error_message = f"[{file_index+1}/{total_files}] 处理 {file_path} 失败: {str(e)}"
            await log("error", error_message)
            failed_results.append({
                "file_path": file_path,
                "error": str(e)
            })
            await report_progress(100, 100, f"失败 {file_path}")
            return False
    
    # 使用任务列表处理所有文件
    tasks = []
    for i, file_path in enumerate(file_paths):
        task = asyncio.create_task(process_single_file(i, file_path))
        tasks.append(task)
    
    # 等待所有任务完成
    await asyncio.gather(*tasks)
    
    # 报告总体进度完成
    progress_notification = types.ProgressNotification(
        method="notifications/progress",
        params=types.ProgressNotificationParams(
            progressToken="batch_overall",
            progress=100.0,
            total=100.0,
            message="批量转换完成"
        )
    )
    await context.session.send_notification(progress_notification)
    
    # 生成总结
    success_count = len(success_results)
    failed_count = len(failed_results)
    
    summary_lines = [
        f"批量转换结果：共 {total_files} 个文件，成功 {success_count} 个，失败 {failed_count} 个",
        ""
    ]
    
    if success_count > 0:
        summary_lines.append("✅ 成功转换的文件：")
        for i, result in enumerate(success_results):
            summary_lines.append(f"[{i+1}] {result['file_path']}")
    
    if failed_count > 0:
        summary_lines.append("")
        summary_lines.append("❌ 转换失败的文件：")
        for i, result in enumerate(failed_results):
            summary_lines.append(f"[{i+1}] {result['file_path']} - 错误: {result['error']}")
    
    # 提供详细结果
    detailed_results = []
    if success_count > 0:
        detailed_results.append("=== 成功转换详情 ===")
        for result in success_results:
            detailed_results.append(f"\n--- {result['file_path']} ---\n{result['summary']}")
    
    return [
        types.TextContent(
            type="text",
            text="\n".join(result_info)
        ),
        types.TextContent(
            type="text",
            text="\n".join(summary_lines)
        ),
        types.TextContent(
            type="text",
            text="\n".join(detailed_results)
        )
    ]

async def convert_document(file_path: str, format: str, output_dir: str = "") -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    result_info = []
    context = app.request_context
    
    async def log(level: str, message: str, add_to_result: bool = True):
        """记录日志并可选择添加到结果信息中"""
        print(f"log: {message}")
        log_message = types.LoggingMessageNotification(
            method="notifications/message",
            params=types.LoggingMessageNotificationParams(
                level=getattr(types.LoggingLevel, level.lower(), "info"),
                data=message
            )
        )
        await context.session.send_notification(log_message)
        if add_to_result:
            result_info.append(message)
    
    async def handle_error(message: str, error_class=RuntimeError):
        """处理错误：记录日志并抛出异常"""
        print(f"error: {message}")
        await log("error", message)
        raise error_class(message)
    
    # 参数验证
    if not file_path:
        raise ValueError("未提供文件路径或URL。请指定file_path参数。")
    
    if not format:
        raise ValueError("未指定目标格式。请使用format参数指定转换格式（docx或png）。")
    
    # 检查是否是URL
    is_url = file_path.startswith(("http://", "https://"))
    
    # 如果是本地文件，验证文件存在
    if not is_url and not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    # 获取API配置
    api_key = os.getenv("API_KEY")
    if not api_key:
        await handle_error("未找到API_KEY。请在客户端配置API_KEY环境变量。")
    
    api_base_url = os.getenv("API_BASE_URL", "https://techsz.aoscdn.com/api/tasks/document/conversion")
    
    # 生成输出文件路径
    if is_url:
        # 从URL中提取文件名
        import urllib.parse
        url_path = urllib.parse.urlparse(file_path).path
        file_name = os.path.splitext(os.path.basename(url_path))[0]
        
        # 如果文件名为空（URL没有明确的文件名），使用一个默认名称
        if not file_name:
            import time
            file_name = f"pdf_converted_{int(time.time())}"
        
        # 确定输出目录
        if not output_dir:
            output_dir = os.getcwd()  # 默认使用当前工作目录
    else:
        # 如果未指定输出目录，使用输入文件所在目录
        if not output_dir:
            output_dir = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    output_name = f"{file_name}.{format}"
    output_path = os.path.join(output_dir, output_name)
    
    # 执行转换
    source_desc = "URL" if is_url else "文件"
    await log("info", f"开始转换：{source_desc} {file_path} -> {output_path}")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 处理URL：先下载到本地临时文件
        temp_file_path = None
        try:
            if is_url:
                await log("info", f"从URL下载文件: {file_path}")
                # 创建临时目录（如果不存在）
                import tempfile
                temp_dir = tempfile.gettempdir()
                os.makedirs(temp_dir, exist_ok=True)
                
                # 生成临时文件名
                import uuid
                temp_filename = f"pdf_download_{uuid.uuid4().hex}.pdf"
                temp_file_path = os.path.join(temp_dir, temp_filename)
                
                # 下载文件
                download_response = await client.get(file_path)
                if download_response.status_code != 200:
                    await handle_error(f"下载URL文件失败。状态码: {download_response.status_code}")
                
                # 保存到临时文件
                with open(temp_file_path, "wb") as f:
                    f.write(download_response.content)
                
                await log("info", f"文件已下载到临时位置: {temp_file_path}")
                
                # 使用临时文件替代URL
                file_to_use = temp_file_path
            else:
                file_to_use = file_path
            
            # 1. 上传文件创建转换任务
            await log("info", "上传文件并创建转换任务...")
            
            headers = {"X-API-KEY": api_key}
            data = {"format": format}
            
            # 上传本地文件创建任务
            with open(file_to_use, "rb") as f:
                files = {"file": f}
                response = await client.post(
                    api_base_url,
                    files=files,
                    data=data,
                    headers=headers
                )
            
            if response.status_code != 200:
                await handle_error(f"创建任务失败。状态码: {response.status_code}\n响应: {response.text}")
            
            result = response.json()
            await log("info", f"任务创建成功: {json.dumps(result, ensure_ascii=False)}")
            
            # 2. 获取任务ID
            if "data" not in result or "task_id" not in result["data"]:
                await handle_error(f"无法获取任务ID。API响应：{json.dumps(result, ensure_ascii=False)}")
            
            task_id = result["data"]["task_id"]
            await log("info", f"任务ID: {task_id}")
            
            # 3. 轮询任务状态
            MAX_ATTEMPTS = 100
            for attempt in range(MAX_ATTEMPTS):
                # 报告进度
                progress_notification = types.ProgressNotification(
                    method="notifications/progress",
                    params=types.ProgressNotificationParams(
                        progressToken=task_id,
                        progress=float(attempt),
                        total=float(MAX_ATTEMPTS)
                    )
                )
                await context.session.send_notification(progress_notification)
                
                await asyncio.sleep(3)
                
                status_msg = f"检查任务状态 ({attempt+1}/{MAX_ATTEMPTS})..."
                await log("debug", status_msg)
                
                status_response = await client.get(
                    f"{api_base_url}/{task_id}",
                    headers=headers
                )
                
                if status_response.status_code != 200:
                    await log("warning", f"获取任务状态失败。状态码: {status_response.status_code}")
                    continue
                
                status_result = status_response.json()
                
                # 检查state字段：1表示完成，负数表示失败
                state = status_result.get("data", {}).get("state")
                state_detail = status_result.get("data", {}).get("state_detail", "Unknown")
                progress = status_result.get("data", {}).get("progress", 0)
                
                await log("info", f"当前状态: {state_detail} (state={state}, progress={progress}%)")
                
                # 检查是否完成
                if state == 1:
                    # 尝试直接从当前状态响应中获取下载链接
                    download_url = status_result.get("data", {}).get("file")
                    
                    if not download_url:
                        await handle_error(f"任务完成但未找到下载链接。任务状态：{json.dumps(status_result, ensure_ascii=False)}")
                    
                    await log("info", f"下载文件: {download_url}")
                    download_response = await client.get(download_url)
                    
                    if download_response.status_code != 200:
                        await handle_error(f"下载失败。状态码: {download_response.status_code}")
                    
                    with open(output_path, "wb") as f:
                        f.write(download_response.content)
                    
                    await log("info", f"[OK] 文件已保存至: {output_path}")
                    
                    # 读取转换后的文件信息
                    file_size = os.path.getsize(output_path)
                    file_size_kb = file_size / 1024
                    
                    # 报告完成进度
                    progress_notification = types.ProgressNotification(
                        method="notifications/progress",
                        params=types.ProgressNotificationParams(
                            progressToken=task_id,
                            progress=float(MAX_ATTEMPTS),
                            total=float(MAX_ATTEMPTS)
                        )
                    )
                    await context.session.send_notification(progress_notification)
                    
                    summary = f"[成功] 源{source_desc}已成功转换！\n\n" \
                              f"* 下载地址: {download_url}\n" \
                              f"* 保存位置: {output_path}\n" \
                              f"* 文件大小: {file_size_kb:.2f} KB"
                    
                    return [
                        types.TextContent(
                            type="text",
                            text="\n".join(result_info)
                        ),
                        types.TextContent(
                            type="text",
                            text=summary
                        )
                    ]
                
                elif state < 0:  # 失败
                    await handle_error(f"任务失败: {json.dumps(status_result, ensure_ascii=False)}")
        
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    await log("debug", f"已删除临时文件: {temp_file_path}", add_to_result=False)
                except Exception as e:
                    await log("warning", f"删除临时文件失败: {e}", add_to_result=False)
        
        # 如果代码执行到这里，说明超过了最大尝试次数
        await handle_error(f"超过最大尝试次数（{MAX_ATTEMPTS}），任务未完成", TimeoutError)

async def main():
    import mcp.server.stdio as stdio
    
    async with stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(
                notification_options=NotificationOptions()
            )
        )

def cli_main():
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
