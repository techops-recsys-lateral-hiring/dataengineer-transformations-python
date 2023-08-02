#!/bin/bash

set -euo pipefail

./batect --docker-host=unix://$HOME/.colima/docker.sock integration-test
