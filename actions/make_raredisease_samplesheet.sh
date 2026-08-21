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
            SEX_CODE=0;;
    esac
    echo $SEX_CODE
}

SAMPLE_ID="$1"
CASE_ID="$2"
SEX="$3"
FQ_R1="$4"
FQ_R2="$5"
OUT_DIR="$6"

SAMPLESHEET="${OUT_DIR}/samplesheet.csv"

if [ -f $SAMPLESHEET ]; then
    echo >&2 "warning: samplesheet already exists for sample ${SAMPLE_ID}, delete it if you want to recreate it: ${SAMPLESHEET}"
    exit 1
fi

SEX_CODE=$(sex_to_int "$SEX")

IFS=',' read -r -a FQ1 <<< "$FQ_R1"
IFS=',' read -r -a FQ2 <<< "$FQ_R2"

FQ1_SORT=( $(IFS=$'\n'; echo "${FQ1[*]}" | sort))
FQ2_SORT=( $(IFS=$'\n'; echo "${FQ2[*]}" | sort))

if [ ${#FQ1_SORT[@]} != ${#FQ2_SORT[@]} ]; then
    echo >&2 "warning: Differing number of R1 and R2 fastq files for ${SAMPLE_ID}"
    exit 1
fi

echo "sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id" > ${SAMPLESHEET}
for N in $(seq 0 $((${#FQ1_SORT[@]} - 1))); do
    LANE=$(echo ${FQ1_SORT[$N]} | grep -Po '(?<=_)L\d{3}(?=_)')
    echo ${SAMPLE_ID},${LANE},${FQ1_SORT[$N]},${FQ2_SORT[$N]},${SEX_CODE},2,,,$CASE_ID >> ${SAMPLESHEET}
done
