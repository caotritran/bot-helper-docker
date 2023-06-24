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

DOCBAO_APIKEY = os.environ.get('DOCBAO_APIKEY')


class DOCBAO(BotPlugin):
    """
    Help us to intergrate with docbao, syntax: /docbao <number_of_news>
    """
    
    @botcmd(split_args_with=None)
    def docbao(self, msg, args):
        """_syntax: /docbao <number_of_news>"""
        if len(args) < 1 or len(args) > 1:
            text = "`invalid syntax, _syntax: /docbao <number_of_news>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return
        num = args[0]
        if not num.isnumeric():
            text = "`Must be interger, ex: 1, 2, 3...`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        table = []
        header = ["Title", "Link"]

        url = "https://newsdata.io/api/1/news?country=vi&category=top&apikey={}".format(DOCBAO_APIKEY)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = json.loads(response.text)

        for i in range(0, int(num)):
            title = data['results'][i].get('title')
            link = data['results'][i].get('link')

            table.append([
                            title,
                            link,
                        ])

        result = tabulate(table, headers=header, tablefmt="orgtbl")

        self._bot.send_simple_reply(msg, result, threaded=True)
    