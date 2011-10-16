#!/bin/sh

server=urlmon@107.20.248.100
target_dir=/tmp/urlmon 

rsync -avz --exclude-from=.gitignore ./ $server:$target_dir/
ssh $server << EOF
cd $target_dir
./fcgi.py restart
EOF
