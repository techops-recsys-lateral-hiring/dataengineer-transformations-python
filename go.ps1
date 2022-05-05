$ErrorActionPreference = "Stop"

$action=$args[0]

function Get-Usage {
    Write-Host $MyInvocation.PSCommandPath " <command> [--] [options ...]"
    Write-Host "Commands:"
    Write-Host "    linting   Static analysis, code style, etc."
    Write-Host "    precommit Run sensible checks before committing"
    Write-Host "    install-with-docker-desktop       Install the application requirements along with docker desktop"
    Write-Host "    run-local-unit-test     Run unit tests on local machine"
    Write-Host "    run-docker-desktop-unit-test     Run unit tests on containers using Docker Desktop"
    Write-Host "    run-local-integration-test     Run integration tests on local machine"
    Write-Host "    run-docker-desktop-integration-test     Run integration tests on containers using Docker Desktop"
    Write-Host "    run-local-job     Run job on local machine"
    Write-Host "    run-docker-desktop-job     Run job on containers using Docker Desktop"
}

switch ($action)
{
    linting {
        scripts/win/linting.ps1
        Break
        }
    precommit {
        Write-Host "Precommit Checks"
        Break
        }
    install-with-docker-desktop {
        scripts/win/install_with_docker_desktop.ps1
        Break
        }
    run-local-unit-test {
        Write-Host  "Running unit tests on local machine"
        poetry run pytest tests/unit
        Break
        }
    run-docker-desktop-unit-test {
        Write-Host  "Running unit tests on containers using Docker Desktop"
        ./batect unit-test
        Break
        }
    run-local-integration-test {
        Write-Host "Running integration tests on local machine"
        scripts/win/run-local-integration-test.ps1
        Break
        }
    run-docker-desktop-integration-test {
        Write-Host "Running integration tests on containers using Docker Desktop"
        scripts/win/run-docker-desktop-integration-test.ps1
        Break
        }
    run-local-job {
        Write-Host "Running job on local machine"
       ./scripts/win/run-job.ps1
        Break
        }
    run-docker-desktop-job {
        "Running job on containers using Docker Desktop"
        ./scripts/win/run-docker-desktop-job.ps1
        Break
        }
    usage {
        Get-Usage
        Break
        }
    default {
        Get-Usage
        Break
        }
}