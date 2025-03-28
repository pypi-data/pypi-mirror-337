from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
import mcp.types as types
import httpx
import os
import json
import asyncio

# 加载环境变量
load_dotenv()

app = FastMCP(
    name="lightpdf_convert_document",
    instructions="PDF文档转换工具，支持将PDF转换为DOCX或PNG格式。",
    debug=True,
    log_level="INFO",
)

@app.tool(
    description="将PDF文档转换为其他格式，如DOCX或PNG。"
)
async def convert_document(file_path: str, format: str, context: Context) -> list[str]:
    """将PDF文档转换为其他格式。

    Args:
        file_path: 要转换的PDF文件路径
        format: 目标格式，支持docx、png
        context: MCP上下文对象，用于日志和进度报告

    Returns:
        转换结果信息列表：[进度日志, 结果摘要]
    """
    result_info = []

    async def log(level: str, message: str, add_to_result: bool = True):
        """记录日志并可选择添加到结果信息中"""
        print(f"log: {message}")
        log_func = getattr(context, level)
        await log_func(message)
        if add_to_result:
            result_info.append(message)

    async def handle_error(message: str, error_class=RuntimeError):
        """处理错误：记录日志并抛出异常"""
        print(f"error: {message}")
        await log("error", message)
        raise error_class(message)

    # 参数验证
    if not file_path:
        raise ValueError("未提供文件路径。请指定file_path参数。")

    if not format:
        raise ValueError("未指定目标格式。请使用format参数指定转换格式（docx或png）。")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")

    # 获取API配置
    api_key = os.getenv("API_KEY")
    if not api_key:
        await handle_error("未找到API_KEY。请在客户端配置API_KEY环境变量。")

    api_base_url = os.getenv("API_BASE_URL", "https://techsz.aoscdn.com/api/tasks/document/conversion")
    
    # 生成输出文件路径
    output_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_name = f"{file_name}.{format}"
    output_path = os.path.join(output_dir, output_name)
    
    # 执行转换
    await log("info", f"开始转换：{file_path} -> {output_path}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 上传文件并创建转换任务
        await log("info", "上传文件并创建转换任务...")

        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"format": format}
            headers = {"X-API-KEY": api_key}

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
        await context.report_progress(0, MAX_ATTEMPTS)
        for attempt in range(MAX_ATTEMPTS):
            await asyncio.sleep(3)
            await context.report_progress(attempt + 1, MAX_ATTEMPTS)

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

                await context.report_progress(MAX_ATTEMPTS, MAX_ATTEMPTS)
                return [
                    "\n".join(result_info),
                    f"[成功] 文件已成功转换！\n\n"
                    f"* 下载地址: {download_url}\n"
                    f"* 保存位置: {output_path}\n"
                    f"* 文件大小: {file_size_kb:.2f} KB"
                ]

            elif state < 0:  # 失败
                await handle_error(f"任务失败: {json.dumps(status_result, ensure_ascii=False)}")

        await handle_error(f"超过最大尝试次数（{MAX_ATTEMPTS}），任务未完成", TimeoutError)

def main():
    app.run()
