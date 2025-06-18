import asyncio
import json
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from excel_handler import ExcelHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ExcelMCPServer:
    def __init__(self):
        self.server = Server("excel-medical-claims")
        self.excel_handler = None
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools for querying Excel data"""
            return [
                types.Tool(
                    name="get_data_summary",
                    description="Get basic summary of the medical claims data",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                types.Tool(
                    name="query_claims_data",
                    description="Query the medical claims data with specific parameters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query_type": {
                                "type": "string",
                                "description": "Type of query: basic_stats, sample_data, column_values, filter_data",
                            },
                            "column": {
                                "type": "string",
                                "description": "Column name for column-specific queries",
                            },
                            "value": {
                                "type": "string",
                                "description": "Value to filter by",
                            },
                            "rows": {
                                "type": "integer",
                                "description": "Number of rows to return (for sample_data)",
                                "default": 5
                            }
                        },
                        "required": ["query_type"],
                    },
                ),
                types.Tool(
                    name="get_column_info",
                    description="Get detailed information about all columns in the dataset",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent]:
            """Handle tool calls"""
            if not self.excel_handler:
                return [types.TextContent(type="text", text="Excel data not loaded")]
            
            if name == "get_data_summary":
                result = self.excel_handler.get_data_summary()
            elif name == "query_claims_data":
                query_type = arguments.get("query_type", "")
                result = self.excel_handler.query_data(
                    query_type=query_type,
                    column=arguments.get("column"),
                    value=arguments.get("value"),
                    rows=arguments.get("rows", 5)
                )
            elif name == "get_column_info":
                result = json.dumps(self.excel_handler.get_column_info(), indent=2)
            else:
                result = f"Unknown tool: {name}"
            
            return [types.TextContent(type="text", text=result)]

    async def initialize(self, excel_file_path: str):
        """Initialize the Excel handler"""
        try:
            self.excel_handler = ExcelHandler(excel_file_path)
            print("Excel data loaded successfully")
        except Exception as e:
            print(f"Failed to load Excel data: {e}")
            raise

async def main():
    excel_file_path = os.getenv("EXCEL_FILE_PATH", "your_excel_file.xlsx")
    
    server_instance = ExcelMCPServer()
    await server_instance.initialize(excel_file_path)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="excel-medical-claims",
                server_version="0.1.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())