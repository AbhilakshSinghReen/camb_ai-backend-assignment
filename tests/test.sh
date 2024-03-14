#!/bin/bash

copy_common_files() {
    echo "Copying common files."

    cp ../common/redis_client.py ../server/src/
    # cp ../common/tasks.py src/
}

# delete_common_files() {
#     echo "Cleaning up common files."

#     rm src/redis_client.py
#     rm src/tasks.py
# }

# cleanup() {
#     delete_common_files
# }

# trap cleanup INT

copy_common_files

# echo "Starting server ..."
# python3 main.py
