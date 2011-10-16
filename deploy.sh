#!/bin/sh

server=urlmon@107.20.248.100
virtual_dir=$1
echo "Deploying to /$virtual_dir"
target_dir="/tmp/urlmon/$virtual_dir"

rsync -avz --exclude-from=.gitignore ./ "$server:$target_dir/"
ssh $server << EOF
cd "$target_dir"
./fcgi.py restart $virtual_dir
EOF
