import requests
import json
import time
from pync import Notifier

class StockIndicators:
    """
    Details of a stock's indicators
    """
    def __init__(self, stock):
        """
        Initialises the StockIndicators object
        Args:
            stock (string): The tick of the stock. eg: "AAPL"
        """
        self.stock = stock
        
    def sma(self,stock=None,interval="daily",time_periods=["20","50","200"]):
        """
        API request for the simple moving average (SMA).
        Args:
            stock (string): The tick of the stock. eg: "AAPL"
            interval (string): The time interval used to calculate the SMA.
                               eg: "daily"
            time_periods (list[string]): The time periods used to calculate the SMA
        
        Returns:
            sma_indicators (dict{string:dict}): The SMA
            eg: {'20': {'SMA': '392.4239'}, '50': {'SMA': '364.7128'}, '200': {'SMA': '302.7866'}}
        """
        sma_indicators = {}
        stock = self.stock
        for time_period in time_periods:
            response = requests.get("https://www.alphavantage.co/query?function=SMA&symbol="+stock+"&interval="+interval+"&time_period="+time_period+"&series_type=open&apikey=")
            sma_indicators[time_period] = response.json()['Technical Analysis: SMA']
            sma_values = sma_indicators[time_period].values()
            sma_values_iterator = iter(sma_values)
            most_recent_sma = next(sma_values_iterator)
            sma_indicators[time_period] = most_recent_sma
        return sma_indicators
        
    def rsi(self,stock=None,interval="daily",time_periods=["14"]):
        """
        API request for the RSI.
        Args:
            stock (string): The tick of the stock. eg: "AAPL"
            interval (string): The time interval used to calculate the RSI.
                               eg: "daily"
            time_periods (list[string]): The time period used to calculate RSI
        
        Returns:
            rsi_indicator (dict{string:string}): The RSI value
                                                 eg: {'RSI': '72.6361'}
        """
        stock = self.stock
        for time_period in time_periods:
            response = requests.get("https://www.alphavantage.co/query?function=RSI&symbol="+stock+"&interval="+interval+"&time_period="+time_period+"&series_type=open&apikey=")
            rsi_indicator = response.json()["Technical Analysis: RSI"]
            rsi_values = rsi_indicator.values()
            rsi_values_iterator = iter(rsi_values)
            most_recent_rsi = next(rsi_values_iterator)
            rsi_indicator = most_recent_rsi
        return rsi_indicator
        
    def support_resistance(self,stock=None,interval="D"):
        """
        API request for the support/resistacne levels.
        Args:    
            stock (string): The tick of the stock. eg: "AAPL"
            interval (string): The time interval used to find support/resistance
        
        Returns:
            support_resistance_levels (list[float]): The support/resistance levels
            eg: [212.00430297851562, 277.14581298828125, 332.5799865722656, 383.3599853515625, 446.54998779296875]
        """
        stock = self.stock
        response = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol='+stock+'&resolution='+interval+'&token=')
        support_resistance_levels = response.json()['levels']
        return support_resistance_levels
        
    def aggregate_indicators(self,stock=None,interval="D"):
        """
        API request to get aggregate indicators.
        eg: The response from the API example:
                {
                  "technicalAnalysis": {
                    "count": {
                      "buy": 6,
                      "neutral": 7,
                      "sell": 4
                    },
                    "signal": "neutral"
                  },
                  "trend": {
                    "adx": 24.46020733373421,
                    "trending": false
                  }
                }
        """
        stock = self.stock
        response = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol='+stock+'&resolution='+interval+'&token=')
        aggregate_indicators = response.json()
        return aggregate_indicators
        
    def pattern_recognition(self,stock=None,interval="D"):
        stock = self.stock
        response = r = requests.get('https://finnhub.io/api/v1/scan/pattern?symbol='+stock+'&resolution='+interval+'&token=')
        pattern = response.json()
        return pattern
        
    def stock_quote(self,stock=None):
        """
        Args:    
            stock (string): The tick of the stock. eg: "AAPL"
        
        Returns:
            quote (dict{string:float}): The open, high, low, current, and 
                                        previous current price of the stock.
            eg: {
                  "c": 261.74,
                  "h": 263.31,
                  "l": 260.68,
                  "o": 261.07,
                  "pc": 259.45,
                  "t": 1582641000 
                }
        """
        stock = self.stock
        response = requests.get('https://finnhub.io/api/v1/quote?symbol='+stock+'&token=')
        quote = response.json()
        return quote
        
class StockNotifier:
    """
    Creates stock notifiers
    """
    def __init__(self,stock):
        """
        Initialises the StockNotifer object
        Args:
            stock (string): The tick of the stock. eg "AAPL"
        """
        self.stock = stock
        self.indicators = StockIndicators(self.stock)
        
    def sell_notification_alert(self):
        """
        Sell notification comprises of: 
            1) rsi goes beyond 70. 
            2) rsi goes beyond 80.
            3) sma 200 crosses and drops below sma 50
            4) If stock price is approaching resistance
            2 and 4 are very important
            
        Returns:
            sell_alert_data (dict): The sell alert data
        """
        OVER_SOLD_LEVEL1 = 70
        OVER_SOLD_LEVEL2 = 80
        MARGIN = 1
        sell_alert_data = {}
        
        rsi_indicator = self.indicators.rsi()
        if float(rsi_indicator['RSI']) > OVER_SOLD_LEVEL1:
            rsi_sell_indicator = True
            sell_alert_data['RSI'] = rsi_sell_indicator
            
        sma_indicator = self.indicators.sma()
        sma_200 = float(sma_indicator['200']['SMA'])
        sma_50 = float(sma_indicator['50']['SMA'])
        if sma_200 > sma_50 and (sma_200 - sma_50) < 0.1:
            sma_sell_indicator = True
            sell_alert_data['SMA'] = sma_sell_indicator
        print(rsi_indicator)
        print(sma_indicator)
        
        resistance_levels = self.indicators.support_resistance()
        current_stock_price = self.indicators.stock_quote()['c']
        for resistance_level in resistance_levels:
            if (resistance_level - current_stock_price) < MARGIN:
                #AND > 0
                approaching_resistance = True
                sell_alert_data['SRL'] = approaching_resistance
        # print(support_resistance_indicator)
        # print(indicators.stock_quote())
        return sell_alert_data
    
    def buy_notification_alert(self):
        """
        Buy notification consists of:
            1. RSI is below 70
            2. Current stock price is just above support level
            
        Returns:
            support (float): The closest support level
            current_stock_price (float): The current stock price
            approaching_support (bool) Is the price within a margin of the support?
            eg: (383.3599853515625, 444.45, False)
        """
        OVER_BOUGHT_LEVEL = 70
        MARGIN = 1.02
        buy_alert_data = {}
        approaching_support = False
        rsi_buy_indicator = False
        support_levels = []
        
        rsi_indicator = self.indicators.rsi()
        if float(rsi_indicator['RSI']) < OVER_BOUGHT_LEVEL:
            rsi_buy_indicator = True
            
        support_resistance_levels = self.indicators.support_resistance()
        current_stock_price = self.indicators.stock_quote()['c']
        [support_levels.append(level) for level in support_resistance_levels if current_stock_price > level]    
        support = min(support_levels,key=lambda support_level: abs(support_level - current_stock_price)) 
        if (current_stock_price/support) <= MARGIN and rsi_buy_indicator:
            approaching_support = True
        return  support, current_stock_price, approaching_support
         
    def aggregate_notification_alert(self):
        """
        Notification based on aggregate indicators.
        Retuns:
            aggregator_buy (bool): The buy count based on 17 indicators
            aggregator_sell (bool): The sell count based on 17 indicators
            adx (float): The adx of the trend
        """
        MINIMUM_PERCENTAGE = 0.8
        aggregator = self.indicators.aggregate_indicators()
        print(aggregator)
        aggregator_tech_analysis = aggregator['technicalAnalysis']['count']
        tech_analysis_buy = aggregator_tech_analysis['buy']
        tech_analysis_neu = aggregator_tech_analysis['neutral']
        tech_analysis_sell = aggregator_tech_analysis['sell']
        aggregator_buy, aggregator_sell = False, False
        if tech_analysis_buy/(tech_analysis_buy+tech_analysis_neu+tech_analysis_sell) > MINIMUM_PERCENTAGE:
            aggregator_buy = True
        if tech_analysis_sell/(tech_analysis_buy+tech_analysis_neu+tech_analysis_sell) > MINIMUM_PERCENTAGE:
            aggregator_sell = True
        adx = aggregator['trend']['adx']
        
        return aggregator_buy, aggregator_sell, round(adx,3)

class NotificationControls:
    """
    Controller of all notifications
    """
    appIcons = {
        'AAPL': "https://img.icons8.com/dusk/2x/mac-os.png",
        'MSFT': "https://img.icons8.com/dusk/2x/windows-logo.png",
        'FB': "https://img.icons8.com/nolan/2x/facebook-new.png",
        'TSLA': "https://img.icons8.com/color/2x/tesla-logo.png",
        'KL': "https://img.icons8.com/dusk/2x/gold-bars.png",
        'CTC.A': "https://img.icons8.com/dusk/2x/wheel.png",
        'TECK': "https://img.icons8.com/nolan/2x/mine-cart.png",
    }
    
    def __init__(self, interested_stocks,stock_notifiers={}):
        """
        Initialises the NotificationControls object.
        Args:
            interested_stocks (list[string]): A list of stock of interest.
                                          eg: ["AAPL","MSFT","FB"]
            stock_notifiers (dict(StockNotifer)): A dictionary of StockNotifer objects
        """
        self.stock_notifiers = stock_notifiers
        self.interested_stocks = interested_stocks
        # self.stock = stock
    
    def add_stock_notifier(self,stock_notifier):
        """
        For now assume we are only adding buy_notification_alerts.
        Args:
            stock_notifier (StockNotifer): A StockNotifer object
        """
        self.stock_notifiers[stock_notifier.stock] = stock_notifier.buy_notification_alert()
    
    def control_notifiers(self):
        """
        Separate the notifications so in the event that multiple notifications
        are triggered enough time is delegated for the user to read.        
        """
        WAIT_TIME = 8
        for stock in self.interested_stocks:
            notifier = StockNotifier(stock)
            self.add_stock_notifier(notifier)
            if self.stock_notifiers[notifier.stock][-1]:
                Notifier.notify(f'Current Price @ ${self.stock_notifiers[notifier.stock][1]}', title=f'{stock} BUY', appIcon=NotificationControls.appIcons[stock])
                time.sleep(WAIT_TIME)
                

if __name__ == '__main__':
    stocks = ['AAPL','MSFT','FB','KL','TECK']
    NotificationControls(interested_stocks=stocks).control_notifiers()

# appl_notifier = StockNotifier("AAPL")
# msft_notifier = StockNotifier("MSFT")
# fb_notifier = StockNotifier("FB")
# appl_buy_data = appl_notifier.buy_notification_alert()
# msft_buy_data = msft_notifier.buy_notification_alert()
# fb_buy_data = fb_notifier.buy_notification_alert()
# if appl_buy_data[2]: Notifier.notify(f'Current Price @ ${appl_buy_data[1]}', title="APPL BUY", appIcon="https://img.icons8.com/dusk/2x/mac-os.png") 
# if msft_buy_data[2]: Notifier.notify(f'Current Price @ ${msft_buy_data[1]}', title="MSFT BUY", appIcon="https://img.icons8.com/dusk/2x/windows-logo.png") 
