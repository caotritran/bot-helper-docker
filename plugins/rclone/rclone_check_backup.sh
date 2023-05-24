#!/bin/bash
domain_name=$1

last=$(echo $domain_name | awk -F"." '{print $1}')
last=$(echo $last | awk -F"-" '{print $1}')

if [ ${#last} > 12 ]; then
        last=${last:$i:10}
fi

custom_domain=$last
found=false


for i in `rclone listremotes --config /data/rclone.conf`; do
    rclone ls $i --config /data/rclone.conf | grep $custom_domain > /dev/null 2>&1
    if rclone ls $i --config /data/rclone.conf | grep -q $custom_domain; then
        rclone ls $i --config /data/rclone.conf | grep $custom_domain
        echo "Files backup exists at remote **$i**"
        echo "==================================="
        found=true
    fi
done

if [ "$found" = false ]; then
    echo "Not found: Files backup does not exist for domain $custom_domain"
fi
