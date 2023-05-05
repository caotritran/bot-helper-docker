from ast import arg
import time
from errbot import BotPlugin, botcmd
from sys import exit
import requests, json, urllib3, os, re
from tabulate import tabulate

from dotenv import load_dotenv
from cloudflare import update_dns_recordA
from jenkinsapi.jenkins import Jenkins
import subprocess
#load_dotenv('.env')

JENKINS_API_TOKEN = os.environ.get('JENKINS_API_TOKEN')

class JENKINS(BotPlugin):
    """
    Help us to intergrate with CF API, syntax: /jenkins <cmd>
    """
    
    @botcmd(split_args_with=None)
    def jenkins_findrootip_offshore(self, msg, args):
        """_syntax: /jenkins findrootip offshore <ip>"""
        if len(args) < 1 or len(args) > 1:
            text = "`invalid syntax, _syntax:  /jenkins findrootip offshore <ip>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return
        ip_offshore = args[0]
        URL = "http://jenkins.sweb.vn/job/sweb/job/Check_IP_From_Offshore"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"hosts", "value":"%s"}]}' % (ip_offshore)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(40)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)
            

        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` !!!"
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(40)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)


    @botcmd(split_args_with=None)
    def jenkins_coverip_offshore(self, msg, args):
        """_syntax: /jenkins coverip offshore <domain_name> <root_ip> <offshore_ip>"""
        if len(args) < 3 or len(args) > 3:
            text = "`invalid syntax, _syntax: /jenkins coverip offshore <domain_name> <root_ip>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        domain_name = args[0]
        root_ip = args[1]
        offshore_ip = args[2]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Offshore_Cover/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}, {"name":"RootIP", "value":"%s"}]}' % (offshore_ip, domain_name, root_ip)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            output_text = console_output.text
            
            if re.search("SUCCESS", output_text):
                text = "Cover offshore IP completed!"
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return       

        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` !!!"
            self._bot.send_simple_reply(msg, text, threaded=True)
            # time.sleep(150)
            # console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            # output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)


    @botcmd(split_args_with=None)
    def jenkins_createssl(self, msg, args):
        """_syntax: /jenkins createssl <root_ip> <domain_name>"""
        if len(args) < 3 or len(args) > 3:
            text = "`invalid syntax, _syntax: /jenkins createssl <root_ip> <domain_name>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        root_ip = args[0]
        domain_name = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Create_SSL/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}' % (root_ip, domain_name)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(50)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)
            

        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` !!!"
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(50)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)


    @botcmd(split_args_with=None)
    def jenkins_createssl(self, msg, args):
        """_syntax: /jenkins createssl <root_ip> <domain_name>"""
        if len(args) < 2 or len(args) > 2:
            text = "`invalid syntax, _syntax: /jenkins createssl <root_ip> <domain_name>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        root_ip = args[0]
        domain_name = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Create_SSL/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (root_ip, domain_name)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(50)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            if re.search("SUCCESS", output_text):
                self._bot.send_simple_reply(msg, output_text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
            

        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` {}!!!".format(response.status_code)
            self._bot.send_simple_reply(msg, text, threaded=True)

    @botcmd(split_args_with=None)
    def jenkins_createvhost(self, msg, args):
        """_syntax: /jenkins createvhost <root_ip> <domain_name>"""
        if len(args) < 2 or len(args) > 2:
            text = "`invalid syntax, _syntax: /jenkins createvhost <root_ip> <domain_name>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        root_ip = args[0]
        domain_name = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Create_vhost/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (root_ip, domain_name)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)

            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            output_text = console_output.text
            
            if re.search("SUCCESS", output_text):
                text = "Create Vhost completed!"
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return       

            # time.sleep(60)
            # console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            # output_text = console_output.text
            # if re.search("SUCCESS", output_text):
            #     self._bot.send_simple_reply(msg, output_text, threaded=True)
            # else:
            #     text = "Build fail roi @tritran14 oi!!!"
            #     self._bot.send_simple_reply(msg, text, threaded=True)
            
        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` {}!!!".format(response.status_code)
            self._bot.send_simple_reply(msg, text, threaded=True)
            self._bot.send_simple_reply(msg, output_text, threaded=True)

    @botcmd(split_args_with=None)
    def jenkins_backupweb(self, msg, args):
        """_syntax: /jenkins backupweb <root_ip> <domain_name>"""
        if len(args) < 2 or len(args) > 2:
            text = "`invalid syntax, _syntax: /jenkins backupweb <root_ip> <domain_name>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        root_ip = args[0]
        domain_name = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Create_vhost/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (root_ip, domain_name)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(60)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            if re.search("SUCCESS", output_text):
                self._bot.send_simple_reply(msg, output_text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` {}!!!".format(response.status_code)
            self._bot.send_simple_reply(msg, text, threaded=True)



    @botcmd(split_args_with=None)
    def jenkins_banip(self, msg, args):
        """_syntax: /jenkins banip <vps_ip> <ip_want_to_ban>"""
        if len(args) != 2:
            text = "`invalid syntax, _syntax: /jenkins banip <vps_ip> <ip_want_to_ban>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        vps_ip = args[0]
        ban_ip = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/BanIP/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"VPS_IP", "value":"%s"}, {"name":"BAN_IP", "value":"%s"}]}' % (vps_ip, ban_ip)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(20)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            if re.search("SUCCESS", output_text):
                self._bot.send_simple_reply(msg, output_text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` {}!!!".format(response.status_code)
            self._bot.send_simple_reply(msg, text, threaded=True)

    @botcmd(split_args_with=None)
    def jenkins_unbanip(self, msg, args):
        """_syntax: /jenkins unbanip <vps_ip> <ip_want_to_unban>"""
        if len(args) != 2:
            text = "`invalid syntax, _syntax: /jenkins unbanip <vps_ip> <ip_want_to_unban>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        vps_ip = args[0]
        unban_ip = args[1]

        URL = "http://jenkins.sweb.vn/job/sweb/job/UnBanIP/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"VPS_IP", "value":"%s"}, {"name":"UNBAN_IP", "value":"%s"}]}' % (vps_ip, unban_ip)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            time.sleep(20)
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            if re.search("SUCCESS", output_text):
                self._bot.send_simple_reply(msg, output_text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` {}!!!".format(response.status_code)
            self._bot.send_simple_reply(msg, text, threaded=True)

    @botcmd(split_args_with=None)
    def jenkins_backup_restore(self, msg, args):
        """_syntax: /jenkins backup restore <source_ip> <dest_ip> <domain>"""
        if len(args) != 3:
            text = "`invalid syntax, _syntax: /jenkins backup restore <source_ip> <dest_ip> <domain>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        source_ip = args[0]
        dest_ip = args[1]
        domain = args[2]
        backup_url = "http://jenkins.sweb.vn/job/sweb/job/Backup_website/"
        create_vhost_url = "http://jenkins.sweb.vn/job/sweb/job/Create_vhost/"
        restore_url = "http://jenkins.sweb.vn/job/sweb/job/Restore_website/"
        ssl_url = "http://jenkins.sweb.vn/job/sweb/job/Create_SSL/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data_backup = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (source_ip, domain)

        response = requests.post(backup_url+"/build", headers=headers, data=data_backup, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = backup_url + "/lastBuild/consoleText"
        if response.status_code == 201:
            text = "Send trigger backup to jenkins success - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break

            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text

            for line in output_text.splitlines():
                if re.search("backup was completed", line):
                    backup_link = line[60:-1]
                    text = "Success backup - download manual here: {} - continue restore ...".format(backup_link)
                    self._bot.send_simple_reply(msg, text, threaded=True)
        else:
            text = "Build fail roi @tritran14 oi!!!"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        data_create_vhost = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (dest_ip, domain)

        response = requests.post(create_vhost_url+"/build", headers=headers, data=data_create_vhost, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = create_vhost_url + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Creating vhost - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text
            if re.search("SUCCESS", output_text):
                text = "Create vhost completed - continue restore website ..."
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return

        data_restore = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}, {"name":"SOURCE_URL", "value":"%s"}]}' % (dest_ip, domain, backup_link)

        response = requests.post(restore_url+"/build", headers=headers, data=data_restore, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = restore_url + "/lastBuild/consoleText"
        if response.status_code == 201:
            text = "Send trigger restore to jenkins success - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text

            
            if re.search("SUCCESS", output_text):
                text = "restore was completed - continue point dns to destination IP..."
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return

        state = update_dns_recordA(domain,dest_ip)
        if state == 200:
            text = "update record success, status code {} - continue issue SSL LE...".format(state)
            self._bot.send_simple_reply(msg, text, threaded=True)
        else:
            text = "somethings went wrong, status code {}".format(state)
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        #SSL
        data_ssl = 'json={"parameter": [{"name":"HOSTS", "value":"%s"}, {"name":"Domain", "value":"%s"}]}' % (dest_ip, domain)

        response = requests.post(ssl_url+"/build", headers=headers, data=data_ssl, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = ssl_url + "/lastBuild/consoleText"
        if response.status_code == 201:
            text = "Send trigger issue SSL to jenkins success - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            output_text = console_output.text

            
            if re.search("SUCCESS", output_text):
                text = "Create SSL completed - restore step completed!"
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return

    @botcmd(split_args_with=None)
    def jenkins_offshore_cloudflare(self, msg, args):
        """_syntax: /jenkins offshore cloudflare <domain_name> <root_ip> <offshore_ip>"""
        if len(args) < 3 or len(args) > 3:
            text = "`invalid syntax, _syntax: /jenkins offshore cloudflare <domain_name> <root_ip> <offshore_ip>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        domain_name = args[0]
        root_ip = args[1]
        offshore_ip = args[2]

        URL = "http://jenkins.sweb.vn/job/sweb/job/Offshore_Cloudflare/"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'json={"parameter": [{"name":"Domain", "value":"%s"}, {"name":"RootIP", "value":"%s"}, {"name":"HOSTS", "value":"%s"}]}' % (domain_name, root_ip, offshore_ip)

        response = requests.post(URL+"/build", headers=headers, data=data, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))

        output_url = URL + "/lastBuild/consoleText"

        if response.status_code == 201:
            text = "Send trigger build to jenkins success\nGenarating output - please wait ..."
            self._bot.send_simple_reply(msg, text, threaded=True)
            while True:
                time.sleep(60)
                console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
                output_text = console_output.text[-8:-1]
                if output_text == "SUCCESS":
                    break
            output_text = console_output.text
            
            if re.search("SUCCESS", output_text):
                text = "Cover offshore IP with Cloudflare completed!"
                self._bot.send_simple_reply(msg, text, threaded=True)
            else:
                text = "Build fail roi @tritran14 oi!!!"
                self._bot.send_simple_reply(msg, text, threaded=True)
                return       

        else:
            text = "Send trigger build to jenkins fail\n @tritran14 oi vao check ne` !!!"
            self._bot.send_simple_reply(msg, text, threaded=True)
            # time.sleep(150)
            # console_output = requests.get(output_url, auth=('admin', '{}'.format(JENKINS_API_TOKEN)))
            # output_text = console_output.text
            self._bot.send_simple_reply(msg, output_text, threaded=True)

    @botcmd(split_args_with=None)
    def jenkins_find_domain(self, msg, args):
        """_syntax: /jenkins find domain <root_ip>"""
        if len(args) < 1 or len(args) > 1:
            text = "`invalid syntax, _syntax: /jenkins find domain <root_ip>`"
            self._bot.send_simple_reply(msg, text, threaded=True)
            return

        text = "Waiting search all jobs in Jenkins..."
        self._bot.send_simple_reply(msg, text, threaded=True)

        root_ip = args[0]
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        other_file_path = os.path.join(plugin_path, "jenkins_find_domain_from_ip.py")
        result = subprocess.run(['/usr/bin/python3', other_file_path, root_ip], capture_output=True, text=True)

        while True:
            if result.stdout:
                text = result.stdout
                break
            time.sleep(20)
        self._bot.send_simple_reply(msg, text, threaded=True)

        





