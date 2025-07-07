#!/usr/bin/env bash
# Canary deployment for CriptoSentinel
IMAGE_NAME=${DOCKER_IMAGE:-"myrepo/criptosentinel"}
VERSION=${GITHUB_SHA::7}
CANARY_TAG="canary-${VERSION}"
echo "Building image ${IMAGE_NAME}:${CANARY_TAG}"
docker build -t ${IMAGE_NAME}:${CANARY_TAG} .
echo "Pushing to registry"
docker push ${IMAGE_NAME}:${CANARY_TAG}
echo "Starting canary deployment"
docker-compose -f docker-compose.yml -f docker-compose.canary.yml up -d
