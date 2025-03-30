from mcp.server import Server
import httpx
import logging
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeatherQuery(BaseModel):
    """Parameters for querying weather."""
    city: str

async def serve():
    logger.info("Starting Weather Server...")
    server = Server("WeatherServer")
    logger.info("Weather Server initialized")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        logger.info("Listing available tools")
        return [
            Tool(
                name="query_weather",
                description="Query current weather for a city",
                inputSchema=WeatherQuery.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        logger.info(f"Received weather query request for tool: {name}")
        args = WeatherQuery(**arguments)
        logger.info(f"Querying weather for city: {args.city}")
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "q": args.city,
                        "appid": "f6416664b4ecd8a56da5fd95b8d48641"
                    }
                )
                resp.raise_for_status()  # 检查响应状态
                logger.info(f"Successfully retrieved weather data for {args.city}")
                return [TextContent(type="text", text=str(resp.json()))]
            except Exception as e:
                logger.error(f"Error querying weather: {str(e)}")
                raise

    options = server.create_initialization_options()
    logger.info("Server initialization options created")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Starting server main loop...")
        try:
            await server.run(read_stream, write_stream, options)
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise
        finally:
            logger.info("Server shutdown")