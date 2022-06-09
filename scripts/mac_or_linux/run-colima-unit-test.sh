#!/bin/sh

set -euo pipefail

./batect --docker-host=unix://$HOME/.colima/docker.sock unit-test
