#!/bin/bash

set -euo pipefail

INPUTFILE="$1"
SHEET=$2
OUTPUTDIR="$3"
VERSION=$4
IMAGE="tumor-evolution:${VERSION}"

echo >&2 "INFO: using input file ${INPUTFILE}"
echo >&2 "INFO: using sheet ${SHEET}"
echo >&2 "INFO: using output directory ${OUTPUTDIR}"
echo >&2 "INFO: using docker image ${IMAGE}"

if [ ! -f "$INPUTFILE" ]; then
    echo >&2 "ERROR: file or directory not found: ${INPUTFILE}"
    exit 1
fi

if [ ! -d "$OUTPUTDIR" ]; then
    echo >&2 "ERROR: directory not found: ${OUTPUTDIR}"
    exit 1
fi

if [ $(docker images -q "${IMAGE}" | wc -l) -eq 0 ]; then
    echo >&2 "INFO: image not found, building"
    if [ ! -d "tumor-evolution" ]; then
        git clone https://github.com/gmc-norr/tumor-evolution.git
    fi
    cd tumor-evolution
    git pull --tags origin main
    git checkout "v${VERSION}"
    docker build -t "${IMAGE}" .
    echo >&2 "INFO: docker image built"
fi

docker run \
    -v "${INPUTFILE}:/tumor_evolution/data/follow_up_data.xlsx" \
    -v "${OUTPUTDIR}:/tumor_evolution/reports" \
    --rm \
    "${IMAGE}" \
    --sheet "${SHEET}"
