#!/usr/bin/env bash

set -euo pipefail

function sex_to_int() {
    if [ $# -ne 1 ]; then
        echo "sex_to_int: too few arguments"
        exit 1
    fi
    SEX=$1
    SEX_CODE=0
    case ${SEX} in
        male | Male | MALE | M | m)
            SEX_CODE=1;;
        female | Female | FEMALE | F | f)
            SEX_CODE=2;;
        *)
            echo >&2 "error: invalid sex: ${SEX}"
            exit 1;;
    esac
    echo $SEX_CODE
}

SAMPLE_ID="$1"
CASE_ID="$2"
TYPE="$3"
SEX="$4"
PANELS="$5"
FQ_R1="$6"
FQ_R2="$7"
OUT_DIR="$8"

SAMPLESHEET="${OUT_DIR}/samplesheet.csv"

if [ -f $SAMPLESHEET ]; then
    echo >&2 "warning: samplesheet already exists for sample ${SAMPLE_ID}, delete it if you want to recreate it: ${SAMPLESHEET}"
    exit 1
fi

if [ "$TYPE" != "Konstitutionell" ]; then
    echo >&2 "warning: invalid referral type for $SAMPLE_ID: $TYPE"
    exit 1
fi

if ! echo "$PANELS" | grep -q "HTAD_PAN_WGS_v.1.0"; then
    echo >&2 "warning: HTAD panel not found among panels on worksheet for ${SAMPLE_ID}"
    exit 1
fi

SEX_CODE=$(sex_to_int "$SEX")

IFS=',' read -r -a FQ1 <<< "$FQ_R1"
IFS=',' read -r -a FQ2 <<< "$FQ_R2"

echo "sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id" > ${SAMPLESHEET}
for N in $(seq 0 $((${#FQ1[@]} - 1))); do
    LANE=$(echo ${FQ1[$N]} | grep -Po '(?<=_)L\d{3}(?=_)')
    echo ${SAMPLE_ID},${LANE},${FQ1[$N]},${FQ2[$N]},${SEX_CODE},2,,,$CASE_ID >> ${SAMPLESHEET}
done
