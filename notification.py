#!/usr/bin/python3
from pync import Notifier
import requests
import json
import os

"""
Remember to set Crontab if you want a scheduled notifier. I've set mine to run on an hourly basis.
eg: 0 */1 * * * cd DIRECTORY/OF/NOTIFIER && /Users/mshaio/.virtualenvs/notifier/bin/python3 notification.py
"""
class CrytoNotifier:
    """
    Creates a crypto desktop notifier. This has only been tested on a Mac
    """
    def __init__(self, coins):
        """
        CryptoNotifier initialiser.
        Args:
            coins ([string]): A list of the coin's names of interest.
            eg: ['ethereum','litecoin','bitcoin']
        """
        self.coins = coins
        
    def request_coin_data(self):
        """
        API call to coingecko
        Args: 
            None
        Returns:
            coin_price (dict): The coin prices, 
            eg: {'ethereum':200, 'litecoin':100.2, 'bitcoin':14999.2}
        """
        coins_prices = {}
        for coin in self.coins:
            response = requests.get("https://api.coingecko.com/api/v3/coins/"+str(coin))
            data = response.json()
            coins_prices[str(coin)] = data['market_data']['current_price']['cad']
        return coins_prices
        
coins = ['ethereum','litecoin','bitcoin']
basic_coin_data = CrytoNotifier(coins).request_coin_data()
ethereum_price = basic_coin_data[coins[0]]
litecoin_price = basic_coin_data[coins[1]]
bitcoin_price = basic_coin_data[coins[2]]

Notifier.notify(f'Ethereum @ ${ethereum_price} \nLitecoin @ ${litecoin_price} \nBitcoin @ ${bitcoin_price}')

Notifier.remove(os.getpid())
Notifier.list(os.getpid())