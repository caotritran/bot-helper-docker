from ast import arg
from pydoc import text
import time
from errbot import BotPlugin, botcmd
from sys import exit
import requests, json, urllib3, os, re
import paramiko, socket
from tabulate import tabulate

from dotenv import load_dotenv
load_dotenv('.env')


class SERVER(BotPlugin):
    """
    Help us to intergrate with server, syntax: /server <cmd>
    """
    
    @botcmd(split_args_with=None)
    def server_reboot(self, msg, args):
        """_syntax: /server reboot <ip>"""
        if len(args) < 1 or len(args) > 1:
            text = "`invalid syntax, _syntax: /server reboot <ip>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return
        ip_server = args[0]
        USERNAME="deploy"
        REMOTE_SSH_COMMAND="sudo reboot"
        REMOTE_SERVER_IP=ip_server
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key_path = './id_rsa_deploy'
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client.connect(hostname='{}'.format(REMOTE_SERVER_IP), username='{}'.format(USERNAME), pkey=private_key)
        stdin, stdout, stderr = client.exec_command('{}'.format(REMOTE_SSH_COMMAND))
        text = "Send trigger reboot success"
        self._bot.send_simple_reply(msg, text, threaded=True)
        client.close()

        # Wait for server to come back online
        text = "Waiting for server to come back online..."
        self._bot.send_simple_reply(msg, text, threaded=True)
        while True:
            try:
                client.connect(hostname='{}'.format(REMOTE_SERVER_IP), username='{}'.format(USERNAME), pkey=private_key, timeout=10)
                text = "Server is back online!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                client.close()
                break
            except Exception as e:
                text = "Server is still down. Retrying in 10 seconds..."
                self._bot.send_simple_reply(msg, text, threaded=True)
                time.sleep(10)
        


    