#!/bin/bash

set -euo pipefail

SIMULATOR_ROOT="${1:-}"
ARCHIVES_DIR="${2:-}"

if [[ -z "${SIMULATOR_ROOT}" || -z "${ARCHIVES_DIR}" ]]
then
    echo "Usage: $0 SIMULATOR_ROOT ARCHIVES_DIR"
    exit 1
fi

SIMULATOR_ROOT=$(realpath "${SIMULATOR_ROOT}")
ARCHIVES_DIR=$(realpath "${ARCHIVES_DIR}")

cd $(dirname $0)

mkdir -p knockout/Simulator/

srcomp for-each-match . 32,33,34,35 ${SIMULATOR_ROOT}/script/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/matches/0{32,33,34,35}.yaml knockout/Simulator/

srcomp for-each-match . 36,37 ${SIMULATOR_ROOT}/script/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/matches/0{36,37}.yaml knockout/Simulator/

srcomp for-each-match . 38 ${SIMULATOR_ROOT}/script/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/matches/038.yaml knockout/Simulator/
