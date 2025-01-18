from exchange.okx_client import OKXClient
from utils.calculator import calculate_position_size
from utils.logger import get_logger
import time

logger = get_logger()

class FundingArbitrage:
    def __init__(self, config):
        self.config = config
        self.exchange = OKXClient(
            config['api_key'],
            config['api_secret'],
            config['passphrase'],
            config.get('is_test', False)
        )
        
        # 策略参数
        self.funding_threshold = config['funding_threshold']
        self.spread_threshold = config['spread_threshold']
        self.check_interval = config['check_interval']
        self.trading_pairs = config['trading_pairs']

    def check_arbitrage_opportunity(self, pair):
        """检查套利机会"""
        spot_id = f"{pair}-USDT"
        swap_id = f"{pair}-USDT-SWAP"

        # 获取现货和永续合约价格
        spot_price = self.exchange.get_ticker(spot_id)
        swap_price = self.exchange.get_ticker(swap_id)
        funding_rate = self.exchange.get_funding_rate(swap_id)

        if not all([spot_price, swap_price, funding_rate]):
            return False

        logger.info(f"当前市场状态 - {pair}:")
        logger.info(f"现货价格: {spot_price}")
        logger.info(f"永续价格: {swap_price}")
        logger.info(f"资金费率: {funding_rate}")

        # 检查条件
        if funding_rate > self.funding_threshold:
            price_diff = swap_price - spot_price
            if price_diff > self.spread_threshold:
                return True
        
        return False

    def execute_arbitrage(self, pair):
        """执行套利交易"""
        try:
            position_size = calculate_position_size(
                self.exchange,
                pair,
                self.config['max_position_size']
            )
            
            # TODO: 实现具体的交易逻辑
            logger.info(f"执行套利交易 - {pair}, 仓位大小: {position_size}")
            
        except Exception as e:
            logger.error(f"执行套利失败: {str(e)}")

    def run(self):
        """运行套利策略"""
        logger.info("开始运行套利策略...")
        
        while True:
            try:
                for pair in self.trading_pairs:
                    if self.check_arbitrage_opportunity(pair):
                        self.execute_arbitrage(pair)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"策略运行错误: {str(e)}")
                time.sleep(self.check_interval)
