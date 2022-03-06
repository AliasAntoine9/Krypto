from TradingBot.src.core.ScheduleStrategy import Scheduler
from TradingBot.src.utils.KryptoProperties import KryptoProperties

if __name__ == "__main__":
    KryptoProperties.load_properties()
    CryptoBot = Scheduler()
    CryptoBot.start()
