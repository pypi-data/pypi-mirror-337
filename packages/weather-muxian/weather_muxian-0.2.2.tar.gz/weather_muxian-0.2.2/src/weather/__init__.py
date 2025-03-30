import asyncio
import logging
from .server import serve

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置日志
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting weather service...")
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        raise

if __name__ == "__main__":
    main()