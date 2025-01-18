import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.funding_arbitrage import FundingArbitrage
from utils.logger import setup_logger
import yaml
import time

def load_config():
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    # 设置日志
    logger = setup_logger()
    logger.info("启动资金费率套利程序...")

    # 加载配置
    config = load_config()
    
    try:
        # 初始化套利策略
        arbitrage = FundingArbitrage(config)
        
        # 运行套利程序
        arbitrage.run()
        
    except KeyboardInterrupt:
        logger.info("程序正常退出")
    except Exception as e:
        logger.error(f"程序发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()
