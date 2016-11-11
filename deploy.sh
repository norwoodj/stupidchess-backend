#!/bin/bash -e

source common.sh


function usage {
    echo "${0} [ options ] <commands>"
    echo
    echo "This script is used to deploy various pieces used to run this service in a deployed environment. The commands"
    echo "available are listed below, but they include deploying docker images to a remote registry, deploying an application"
    echo "bundle to a remote file storage service, and deploying a remote application bundle to a server to run the application."
    echo
    echo "Commands:"
    echo "  images <image> [<image> [<image> ...]]  Pushes built image to the configured docker registry"
    echo "  bundle <environment>                    Builds the app bundle for the input environment and deploys it to S3"
    echo "  server <environment> <version>          Deploys a built app bundle to the server running in the input environment"
    echo
    echo "Images:"
    print_deploy_usage_images_list
    echo
    echo "Environments:"
    print_environment_list
    echo
    echo "Options:"
    echo "  --help, -h  Print this usage and exit"
}

function build_docker_compose_template_data {
    local environment=${1}
    local service=${2}
    local images=`get_images_for_service ${service}`

    echo '---'
    echo "${service}${HANDLEBARS_ENV_SUFFIX}: '${environment}'"

    for i in ${images}; do
        local image_version=`get_image_version ${i}`
        echo "${i}${HANDLEBARS_VERSION_SUFFIX}: '${image_version}'"
    done

    echo '---'
}

function render_mustache_template_for_service {
    local mustache_file=${1}
    local environment=${2}
    local service=${3}

    build_docker_compose_template_data ${environment} ${service} | docker run \
        --rm -i \
        -v `pwd`:/opt/mustache \
        -w /opt/mustache \
        ${MUSTACHE_RENDER_IMAGE_NAME} \
        mustache - ${mustache_file}
}

function bundle {
    local environment=${1}
    check_environment_argument ${environment}

    local bundle_name="${PROJECT_NAME}-`get_bundle_version`"
    log_block "Deploying '${bundle_name} bundle to S3"

    mkdir ${bundle_name}
    local deploy_services=`get_services_for_deploy`

    for d in ${deploy_services}; do
        log_line "Adding docker_compose file for service '${d}'"
        cp \
          <(render_mustache_template_for_service \
              `get_deploy_docker_compose_mustache_path_for_service ${d}` \
              ${environment} \
              ${d} \
          ) \
          "${bundle_name}/`get_bundled_docker_compose_name_for_service ${d}`"
    done


    local bundle_zip_archive="${bundle_name}.zip"
    log_line "Creating zip archive: ${bundle_zip_archive}"
    zip ${bundle_zip_archive} ${bundle_name}/* &> /dev/null

    log_line "Uploading zipped application bundle to remote destination"
    upload_application_bundle ${environment} ${bundle_zip_archive}

    log_line "Deleting extra artifacts"
    rm -rf ${bundle_name}
    rm ${bundle_zip_archive}
}

function get_docker_registry_name {
    if [[ ! -z ${DOCKER_REGISTRY_URL} ]]; then
        printf ${DOCKER_REGISTRY_URL}
    else
        printf "Docker Hub"
    fi
}

function do_deploy_image {
    local image=${1}
    local version=`get_image_version ${image}`
    local image_tag=`get_image_tag ${image} ${version}`

    log_block "Deploying ${image_tag} image to `get_docker_registry_name`"
    check_current_image_exists ${image}

    log_line "Tagging `get_current_image_tag ${image}` as ${image_tag}"
    docker tag `get_current_image_tag ${image}` ${image_tag}

    log_line "Pushing ${image_tag}"
    docker push ${image_tag}
}

function images {
    local images=${@}
    check_images_argument 'get_images_for_deploy' ${images}

    if [[ ${1} = 'all' ]]; then
        images=`get_images_for_deploy`

        log_block 'Deploying all images:'
        for i in ${images}; do
            log_line "${i}"
        done

        for i in ${images}; do
            do_deploy_image ${i}
        done
    else
        for i in ${images}; do
            if [[ ${i} != 'all' ]]; then
                do_deploy_image ${i}
            fi
        done
    fi
}

function server {
    local environment=${1}
    local version=${2}

    check_environment_argument ${environment}

    if [[ -z ${version} ]]; then
        log_block 'Application version must be provided!'
        echo
        usage
        exit 1
    fi

    log_block "Deploying application version ${version} to environment ${environment}"

    local bundle_name="${PROJECT_NAME}-${version}"
    local bundle_zip="${bundle_name}.zip"
    local s3_destination="`get_s3_path_for_env ${environment}`/${bundle_zip}"
    local servers=`get_servers_for_env ${environment}`

    for s in ${servers}; do
        log_block "Deploying to server: ${s}"
        ssh ${s} /bin/bash <<EOF
sudo su
cd ${SERVER_BUNDLE_DEPLOY_DESTINATION}
aws s3 cp ${s3_destination} .
unzip -o ${bundle_name} && rm ${bundle_zip}
rm -f ${PROJECT_NAME}-current
ln -s ${bundle_name} ${PROJECT_NAME}-current
EOF
    done
}

function main {
    while [[ ${1} == -* ]]; do
        case ${1} in
            -h | --help)
                usage
                exit 0
            ;;
            -*)
                log_block "Invalid flag '${1}'!"
                echo
                usage
                exit 1
            ;;
        esac
        shift
    done

    local command=${1}
    check_command_argument "${command}" 'images' 'bundle' 'server'

    shift
    ${command} ${@}
}

main ${@}
