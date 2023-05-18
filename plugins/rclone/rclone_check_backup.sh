#!/bin/bash
domain_name=$1

last=$(echo $domain_name | awk -F"." '{print $1}')
last=$(echo $last | awk -F"-" '{print $1}')

if [ ${#last} > 12 ]; then
        last=${last:$i:10}
fi

custom_domain=$last

for i in `rclone listremotes --config /data/rclone.conf`; do
    rclone ls $i --config /data/rclone.conf | grep $custom_domain > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        rclone ls $i --config /data/rclone.conf | grep $custom_domain
        if [[ $? -eq 0 ]]; then
            echo "files backup exist at remote **$i**"
            echo "==================================="
        else
            echo "NOT FOUND OR SOMETHING WENT WRONG, LET CHECK MANUAL ON ONEDRIVE!!!"
        fi
    fi
done
