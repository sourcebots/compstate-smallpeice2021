#!/bin/bash

set -euo pipefail

SIMULATOR_ROOT="${1:-}"
ARCHIVES_DIR="${2:-}"

if [[ -z "${SIMULATOR_ROOT}" || -z "${ARCHIVES_DIR}" ]]
then
    echo "Usage: $0 SIMULATOR_ROOT ARCHIVES_DIR"
    exit 1
fi

SIMULATOR_ROOT="realpath ${SIMULATOR_ROOT}"
ARCHIVES_DIR="realpath ${ARCHIVES_DIR}"

cd $(dirname $0)

srcomp for-each-match . 32-35 ${SIMULATOR_ROOT}/scripts/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/*.yaml league/Simulator/

srcomp for-each-match . 36,37 ${SIMULATOR_ROOT}/scripts/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/*.yaml league/Simulator/

srcomp for-each-match . 38 ${SIMULATOR_ROOT}/scripts/run-comp-match ${ARCHIVES_DIR} {NUMBER} @TLAS

cp ${ARCHIVES_DIR}/*.yaml league/Simulator/
