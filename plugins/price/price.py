from ast import arg
from pydoc import text
import time
from errbot import BotPlugin, botcmd
from sys import exit
import requests, json, urllib3, os, re
import paramiko, socket
from tabulate import tabulate
import subprocess

# from dotenv import load_dotenv
# load_dotenv('.env')

BINANCE_APIKEY = os.environ.get('BINANCE_APIKEY')


class PRICE(BotPlugin):
    """
    Help us to intergrate with price, syntax: /price <number_of_news>
    """
    
    @botcmd(split_args_with=None)
    def price(self, msg, args):
        """_syntax: /price <coin_pair_with_usdt>, ex: /price BTCUSDT"""
        if len(args) < 1 or len(args) > 1:
            text = "`invalid syntax, _syntax: /price <coin_pair_with_usdt>, ex: /price BTCUSDT`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return
        symbol = args[0]
        symbol = symbol.upper()
        if symbol.isnumeric():
            text = "`Must be character, ex: BTCUSDT...`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        def get_binance_price(BINANCE_APIKEY, symbol):
            url = 'https://api.binance.com/api/v3/ticker/price?symbol={0}'.format(symbol)

            headers = {
                'X-MBX-APIKEY': BINANCE_APIKEY
            }

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                price = data['price']
                return price
            except requests.exceptions.RequestException as e:
                print('Error occurred:', e)
                return None

        # Call the function to get the price
        symbol_price = get_binance_price(BINANCE_APIKEY, symbol)
        if symbol_price:
            text = "The price of {0} is: {1}".format(symbol, symbol_price)
            self._bot.send_simple_reply(msg, text, threaded=True)
