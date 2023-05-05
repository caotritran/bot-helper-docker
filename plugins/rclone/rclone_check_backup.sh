#!/bin/bash
domain_name=$1

last=$(echo $domain_name | awk -F"." '{print $1}')
last=$(echo $last | awk -F"-" '{print $1}')

if [ ${#last} > 12 ]; then
        last=${last:$i:10}
fi

custom_domain=$last

for i in `rclone listremotes --config /data/rclone.conf`; do
    rclone ls $i --config /opt/rclone.conf | grep $custom_domain > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        rclone ls $i --config /opt/rclone.conf | grep $custom_domain
        echo "files backup exist at remote **$i**"
        echo "==================================="
    fi
done
