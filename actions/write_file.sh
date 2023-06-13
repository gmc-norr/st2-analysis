FILE_PATH=$1
TEXT="$2"

if [ ! -d $(dirname ${FILE_PATH}) ]; then
    echo >&2 "ERROR: directory not found: $(dirname ${FILE_PATH})"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
FILE_PATH="${FILE_PATH/TIMESTAMP/${TIMESTAMP}}"

echo "${TEXT}" > "${FILE_PATH}"
