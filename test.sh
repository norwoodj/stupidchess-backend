#!/bin/bash -e

source common.sh

image_tag="${PROJECT_NAME}-${SERVER_TESTS_IMAGE_NAME}"

if [[ "$(docker history -q ${image_tag} 2> /dev/null)" == "" ]]; then
    echo "==> ${image_tag} image doesn't exist, building..."
    echo
    docker build -t ${image_tag} -f "${DOCKERFILE_DIRECTORY}/${DOCKERFILE_PREFIX}${SERVER_TESTS_IMAGE_NAME}" .
fi

docker run --rm -i \
    -v $(pwd)/server:/opt/stupidchess/server \
    ${image_tag}
