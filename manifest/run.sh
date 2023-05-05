#!/bin/bash

GIT_COMMITID=${1:-latest}

sed -i "s/COMMIT_ID/$GIT_COMMITID/g" ./deployment.yaml

echo "$GIT_COMMITID"

echo "$CONTEXT - $NAMESPACE" 