from errbot import BotPlugin
from errcron import CrontabMixin
import os, subprocess

TELE_GROUP_ID = os.environ.get('TELE_GROUP_ID')
class ErrcronDemo(CrontabMixin, BotPlugin):
    """
    Remind task daily
    """
    CRONTAB = [
        '0 8 * * * .remind_daily @pikabot',
        '10 8 * * 6 .remind_weekly @pikabot',
        '0 19 * * * .remind_daily_ippoint @pikabot',
    ]

    def activate(self):
        super().activate()

    def remind_daily(self, polled_time, identity):
        identity = TELE_GROUP_ID
        user = self.build_identifier(identity)
        #return self.send(user, 'Currently {}'.format(polled_time.strftime('%H:%M')))
        text = "***Remind***\n" + "1. What are the issues today? - Check tele [Alert] 🤖 Sweb\n" +  "2. What are the complaints or renew payments today? - Check the email\n" + "cc @tritran14 @Cuong"
        return self.send(user, text)

    def remind_weekly(self, polled_time, identity):
        identity = TELE_GROUP_ID
        user = self.build_identifier(identity)
        #return self.send(user, 'Currently {}'.format(polled_time.strftime('%H:%M')))
        text = "***Remind***\n" + "Please check and clear history trash Onedrive !!!\n" + "cc @tritran14"
        return self.send(user, text)
    
    def remind_daily_ippoint(self, polled_time, identity):
        identity = TELE_GROUP_ID
        user = self.build_identifier(identity)
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        other_file_path = os.path.join(plugin_path, "checkippoint.py")
        output = subprocess.check_output(["/opt/bot-helper/venv/bin/python3.8", other_file_path]).decode("utf-8")

        # send output as message
        return self.send(user, output)