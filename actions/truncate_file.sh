FILE_PATH=$1

if [ ! -f "$FILE_PATH" ]; then
    echo >&2 "ERROR: file or directory not found: ${FILE_PATH}"
    exit 1
fi

truncate --no-create --size=0 "${FILE_PATH}"
