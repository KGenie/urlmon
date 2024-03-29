#!/bin/sh

server=urlmon@107.20.248.100
virtual_dir=$1
echo "Deploying to /$virtual_dir"
target_dir="/srv/urlmon/$virtual_dir"

ssh $server << EOF
mkdir -p $target_dir
EOF
rsync -avz --exclude-from=.gitignore ./ "$server:$target_dir/"
ssh $server << EOF
/home/urlmon/start_fcgi.sh $virtual_dir
EOF
