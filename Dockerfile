FROM google/cloud-sdk:alpine

COPY ./requirements.txt /tmp/errbot-requirements.txt

RUN apk add py3-pip tzdata

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev make \
      && mkdir -p /data \
      && pip3 install -r /tmp/errbot-requirements.txt \
      && apk del .build-deps

RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip \
      && unzip rclone-current-linux-amd64.zip \
      && cd rclone-*-linux-amd64 \
      && cp rclone /usr/bin/ \
      && chown root:root /usr/bin/rclone \
      && chmod 755 /usr/bin/rclone

COPY . /data

# VOLUME ./slack-system-bot/plugins /tiki/slack-system-bot/plugins

WORKDIR /data
# TODO: switch to workload identity
# CMD gcloud auth activate-service-account --project=tiki-infra-tf --key-file=$GOOGLE_APPLICATION_CREDENTIALS \
#   && errbot
CMD errbot