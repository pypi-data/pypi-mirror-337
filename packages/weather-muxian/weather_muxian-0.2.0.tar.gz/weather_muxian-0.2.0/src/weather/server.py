from mcp.server import Server
import httpx
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

class WeatherQuery(BaseModel):
    """Parameters for querying weather."""
    city: str

async def serve():
    server = Server("WeatherServer")


    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="query_weather",
                description="Query current weather for a city",
                inputSchema=WeatherQuery.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        args = WeatherQuery(**arguments)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": args.city,
                    "appid": "f6416664b4ecd8a56da5fd95b8d48641"
                }
            )
            # 返回格式化的结果
            return [TextContent(content=resp.text)]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)