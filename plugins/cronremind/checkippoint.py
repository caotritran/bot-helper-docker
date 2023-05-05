import re
import paramiko, socket

list_instance_ips = {   'TDA29': '13.212.52.178', 
                        'TDA30': '52.79.233.147',
                        'TDA31': '52.79.250.150',
                        'TDA32': '3.106.123.192',
                        'TDA33': '18.143.11.232',
                        'TDA34': '54.151.243.169',
                        'TDA35': '18.142.143.104'
                    }

def main():
    
    USERNAME="deploy"
    REMOTE_SSH_COMMAND="find /etc/nginx/conf.d/ -type f -name '*.conf' -print0 | xargs -0 egrep '^(\s|\t)*server_name' | sed -r 's/(.*server_name\s*|;)//g' | tr -s ' ' '\n' | sort | uniq | sed '/^www/d' | grep -Ev '\_|\#|\by|\Certbot|\managed|tda|TDA'"
    OUTPUT_FILE = "output.txt"
    for hostname, instance_ip in list_instance_ips.items():
        REMOTE_SERVER_IP=instance_ip

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key_path = './id_rsa_deploy'
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client.connect(hostname='{}'.format(REMOTE_SERVER_IP), username='{}'.format(USERNAME), pkey=private_key)
        stdin, stdout, stderr = client.exec_command('{}'.format(REMOTE_SSH_COMMAND))

        output = stdout.read().decode('utf-8')
        with open(OUTPUT_FILE, "w") as f:
            f.write(output)
        client.close()
        with open("output.txt", "r") as domains:
            for domain in domains.readlines():
                domain = domain.strip()
                try:
                    ip = socket.gethostbyname(domain)
                    if ip == instance_ip:
            
                        print("- Domain {0} chua boc offshore - IP đang point den {1} - {2}".format(domain, ip, hostname))
                except socket.gaierror:
                    print("- Không thể resolve domain {0}".format(domain))


if __name__ == "__main__":
    main()