#!/bin/bash

set -euo pipefail

./batect --docker-host=unix://$HOME/.colima/docker.sock run-job
