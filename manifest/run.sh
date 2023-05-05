#!/bin/bash

GIT_COMMITID=${1:-latest}

sed -i "s/COMMIT_ID/$GIT_COMMITID/g" ./deployment.yaml

echo "GIT_COMMITID: $GIT_COMMITID"

cat ./deployment.yaml | grep "image"

kubectl config use-context $CONTEXT && kubectl apply -f deployment.yaml -n $NAMESPACE