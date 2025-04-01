# 标准库导入
import asyncio
import os
from typing import List

# 第三方库导入
from dotenv import load_dotenv

# MCP相关导入
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# 本地导入
from .converter import Converter, ConversionResult, Logger, FileHandler

# 加载环境变量
load_dotenv()

# 创建Server实例
app = Server(
    name="lightpdf_convert_document",
    instructions="文档格式转换工具。支持PDF转Word/Excel/PPT/图片/HTML/文本，以及Word/Excel/PPT/图片/CAD/CAJ/OFD转PDF。",
)

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="文档格式转换工具。\n\n支持以下转换：\n- PDF转Word/Excel/PPT/图片/HTML/文本\n- Word/Excel/PPT/图片/CAD/CAJ/OFD转PDF\n\n支持单个或多个本地文件路径或网络URL。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "要转换的文件路径(绝对路径)或网络URL列表"
                    },
                    "format": {
                        "type": "string",
                        "description": "目标格式，支持pdf/docx/xlsx/pptx/png/html/txt",
                        "enum": ["pdf", "docx", "xlsx", "pptx", "png", "html", "txt"]
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
        file_paths = arguments.get("file_paths", [])
        # 如果传入的是字符串，转换为列表
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        format = arguments.get("format", "")
        output_dir = arguments.get("output_dir", "")
        
        # 创建必要的对象
        logger = Logger(app.request_context)
        file_handler = FileHandler(logger)
        converter = Converter(logger, file_handler)
        
        # 对于单个文件，使用简化的输出格式
        if len(file_paths) == 1:
            result = await converter.convert_file(file_paths[0], format, output_dir)
            
            if result.success:
                file_size_kb = result.file_size / 1024
                summary = f"转换成功：\n\n" \
                         f"文件已保存至: {result.output_path}\n" \
                         f"文件大小: {file_size_kb:.2f} KB"
            else:
                error_msg = f"文件转换失败: {result.error_message}"
                await logger.error(error_msg)
            
            return [types.TextContent(
                type="text",
                text=summary
            )]
        
        # 批量处理
        await logger.log("info", f"开始批量转换 {len(file_paths)} 个文件为 {format} 格式")
        
        # 并发处理文件，限制并发数为5
        semaphore = asyncio.Semaphore(5)
        results: List[ConversionResult] = []
        
        async def process_single_file(file_path: str):
            async with semaphore:
                return await converter.convert_file(file_path, format, output_dir)
        
        # 创建任务列表
        tasks = [process_single_file(file_path) for file_path in file_paths]
        results = await asyncio.gather(*tasks)
        
        # 统计结果
        success_count = sum(1 for r in results if r.success)
        failed_count = len(results) - success_count
        
        # 生成报告
        report_lines = [
            f"批量转换结果：共 {len(file_paths)} 个文件，成功 {success_count} 个，失败 {failed_count} 个",
            ""
        ]
        
        # 添加成功的文件信息
        if success_count > 0:
            report_lines.extend(["[成功] 转换成功的文件：", ""])
            for i, result in enumerate(results):
                if result.success:
                    file_size_kb = result.file_size / 1024
                    report_lines.extend([
                        f"[{i+1}] {result.file_path}",
                        f"保存位置: {result.output_path}",
                        f"文件大小: {file_size_kb:.2f} KB",
                        ""
                    ])
        
        # 添加失败的文件信息
        if failed_count > 0:
            report_lines.extend(["[失败] 转换失败的文件：", ""])
            for i, result in enumerate(results):
                if not result.success:
                    report_lines.extend([
                        f"[{i+1}] {result.file_path}",
                        f"错误: {result.error_message}",
                        ""
                    ])
        
        report_msg = "\n".join(report_lines)
        if success_count == 0:
            await logger.error(report_msg)
        
        return [types.TextContent(
            type="text",
            text=report_msg
        )]
    
    error_msg = f"未知工具: {name}"
    await logger.error(error_msg, ValueError)

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
