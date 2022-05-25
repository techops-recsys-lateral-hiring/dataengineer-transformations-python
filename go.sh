#!/bin/bash

set -euo pipefail


function trace() {
    {
        local tracing
        [[ "$-" = *"x"* ]] && tracing=true || tracing=false
        set +x
    } 2>/dev/null
    if [ "$tracing" != true ]; then
        # Bash's own trace mode is off, so explicitely write the message.
        echo "$@" >&2
    else
        # Restore trace
        set -x
    fi
}


function contains () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


# Parse arguments.
operations=()
subcommand_opts=()
while true; do
    case "${1:-}" in
    lint|linting)
        operations+=( linting )
        shift
        ;;
    precommit)
        operations+=( precommit )
        shift
        ;;
    install-with-docker-desktop)
        operations+=( install-with-docker-desktop )
        shift
        ;;
    install-with-colima)
            operations+=( install-with-colima )
            shift
            ;;
    start-colima)
        operations+=( start-colima )
        shift
        ;;
    run-local-unit-test)
        operations+=( run-local-unit-test )
        shift
        ;;
    run-docker-desktop-unit-test)
        operations+=( run-docker-desktop-unit-test )
        shift
        ;;
    run-colima-unit-test)
        operations+=( run-colima-unit-test )
        shift
        ;;
    run-local-integration-test)
        operations+=( run-local-integration-test )
        shift
        ;;
    run-docker-desktop-integration-test)
        operations+=( run-docker-desktop-integration-test )
        shift
        ;;
    run-colima-integration-test)
            operations+=( run-colima-integration-test )
            shift
            ;;
    run-local-job)
        operations+=( run-local-job )
        shift
        ;;
    run-docker-desktop-job)
        operations+=( run-docker-desktop-job )
        shift
        ;;
    run-colima-job)
            operations+=( run-colima-job )
            shift
            ;;
    --)
        shift
        break
        ;;
    -h|--help)
        operations+=( usage )
        shift
        ;;
    *)
        break
        ;;
    esac
done
if [ "${#operations[@]}" -eq 0 ]; then
    operations=( usage )
fi
if [ "$#" -gt 0 ]; then
    subcommand_opts=( "$@" )
fi


function usage() {
    trace "$0 <command> [--] [options ...]"
    trace "Commands:"
    trace "    linting   Static analysis, code style, etc.(please install poetry if you would like to use this command)"
    trace "    precommit Run sensible checks before committing"
    trace "    install-with-docker-desktop       Install the application requirements along with docker desktop"
    trace "    install-with-colima       Install the application requirements along with colima"
    trace "    start-colima     Start Colima"
    trace "    run-local-unit-test     Run unit tests on local machine"
    trace "    run-colima-unit-test     Run unit tests on containers using Colima"
    trace "    run-docker-desktop-unit-test     Run unit tests on containers using Docker Desktop"
    trace "    run-local-integration-test     Run integration tests on local machine"
    trace "    run-colima-integration-test     Run integration tests on containers using Colima"
    trace "    run-docker-desktop-integration-test     Run integration tests on containers using Docker Desktop"
    trace "    run-local-job     Run job on local machine"
    trace "    run-colima-job     Run job on containers using Colima"
    trace "    run-docker-desktop-job     Run job on containers using Docker Desktop"
    trace "Options are passed through to the sub-command."
}


function linting() {
    trace "Linting"
    ./scripts/mac_or_linux/linting.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function precommit() {
    trace "Precommit Checks"
}


function install-with-docker-desktop() {
    trace "Install the application requirements along with docker desktop"
    ./scripts/mac_or_linux/install-with-docker-desktop.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function install-with-colima() {
    trace "Install the application requirements along with docker desktop"
    ./scripts/mac_or_linux/install-with-colima.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function start-colima() {
    trace "Starting Colima"
    ./scripts/mac_or_linux/start-colima.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-local-unit-test() {
    trace "Running unit tests on local machine"
    ./scripts/mac_or_linux/unit-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-colima-unit-test() {
    trace "Running unit tests on containers using Colima"
    ./scripts/mac_or_linux/run-colima-unit-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-docker-desktop-unit-test() {
    trace "Running unit tests on containers using Docker Desktop"
    ./scripts/mac_or_linux/run-docker-desktop-unit-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-local-integration-test() {
    trace "Running integration tests on local machine"
    ./scripts/mac_or_linux/integration-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-colima-integration-test() {
    trace "Running integration tests on containers using Colima"
    ./scripts/mac_or_linux/run-colima-integration-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-docker-desktop-integration-test() {
    trace "Running integration tests on containers using Docker Desktop"
    ./scripts/mac_or_linux/run-docker-desktop-integration-test.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-local-job() {
    trace "Running job on local machine"
    ./scripts/mac_or_linux/run-job.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-colima-job() {
    trace "Running job on containers using Colima"
    ./scripts/mac_or_linux/run-colima-job.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


function run-docker-desktop-job() {
    trace "Running job on containers using Docker Desktop"
    ./scripts/mac_or_linux/run-docker-desktop-job.sh "${subcommand_opts[@]:+${subcommand_opts[@]}}"
}


script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "${script_directory}/"


if contains usage "${operations[@]}"; then
    usage
    exit 1
fi
if contains linting "${operations[@]}"; then
    linting
fi
if contains precommit "${operations[@]}"; then
    precommit
fi
if contains install-with-docker-desktop "${operations[@]}"; then
    install-with-docker-desktop
fi
if contains install-with-colima "${operations[@]}"; then
    install-with-colima
fi
if contains start-colima "${operations[@]}"; then
    start-colima
fi
if contains run-local-unit-test "${operations[@]}"; then
    run-local-unit-test
fi
if contains run-colima-unit-test "${operations[@]}"; then
    run-colima-unit-test
fi
if contains run-docker-desktop-unit-test "${operations[@]}"; then
    run-docker-desktop-unit-test
fi
if contains run-local-integration-test "${operations[@]}"; then
    run-local-integration-test
fi
if contains run-colima-integration-test "${operations[@]}"; then
    run-colima-integration-test
fi
if contains run-docker-desktop-integration-test "${operations[@]}"; then
    run-docker-desktop-integration-test
fi
if contains run-local-job "${operations[@]}"; then
    run-local-job
fi
if contains run-colima-job "${operations[@]}"; then
    run-colima-job
fi
if contains run-docker-desktop-job "${operations[@]}"; then
    run-docker-desktop-job
fi


trace "Exited cleanly."