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

RUN_DIR="$1"
SAMPLE_ID="$2"
CASE_ID="$3"
TYPE="$4"
SEX="$5"
OUT_DIR="$6"

SAMPLESHEET="${OUT_DIR}/samplesheet.csv"

if [ -f $SAMPLESHEET ]; then
    echo >&2 "warning: samplesheet already exists for sample ${SAMPLE_ID}, delete it if you want to recreate it: ${SAMPLESHEET}"
    exit 1
fi

if [ "$TYPE" != "Konstitutionell" ]; then
    echo >&2 "warning: invalid referral type for $SAMPLE_ID: $TYPE, skipping"
    exit 1
fi

#if [ $(echo "$SAMPLE" | jq -r '.Panels // [] | index("HTAD_PAN_WGS_v.1.0") != null') == "false" ]; then
#    echo >&2 "warning: HTAD panel not found among panels on worksheet for ${SAMPLE_ID}, skipping"
#    continue
#fi

SEX_CODE=$(sex_to_int "$SEX")

echo "creating samplesheet for ${SAMPLE_ID} with case id ${CASE_ID}"

# mkdir -p $OUT_DIR

FQ1=($(find "$(realpath ${RUN_DIR}/Analysis/1/Data)" -maxdepth 3 -type f -name "${SAMPLE_ID}*R1*.fastq.gz" | sort))
FQ2=($(find "$(realpath ${RUN_DIR}/Analysis/1/Data)" -maxdepth 3 -type f -name "${SAMPLE_ID}*R2*.fastq.gz" | sort))

echo "sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id" > ${SAMPLESHEET}
for N in $(seq 0 $((${#FQ1[@]} - 1))); do
    LANE=$(echo ${FQ1[$N]} | grep -Po '(?<=_)L\d{3}(?=_)')
    # echo >&2 "error: failed to indentify lane from fastq: ${FQ1}" && continue
    echo ${SAMPLE_ID},${LANE},${FQ1[$N]},${FQ2[$N]},${SEX_CODE},2,,,$CASE_ID
    echo ${SAMPLE_ID},${LANE},${FQ1[$N]},${FQ2[$N]},${SEX_CODE},2,,,$CASE_ID >> ${SAMPLESHEET}
done
