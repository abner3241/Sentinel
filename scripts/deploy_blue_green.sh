#!/usr/bin/env bash
# Blue/Green deployment for CriptoSentinel
IMAGE_NAME=${DOCKER_IMAGE:-"myrepo/criptosentinel"}
VERSION=${GITHUB_SHA::7}
echo "Deploying stable image ${IMAGE_NAME}:${VERSION}"
docker-compose -f docker-compose.yml up -d
