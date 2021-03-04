#!/usr/local/bin/zsh
#!/bin/bash
# get all the files that are ready to commit
# user has executed git add . 

root="/Users/mikeh/home/projects/CodeStoryLessons"

if [ $# -eq 0 ]; then
  out=$(git diff-index --cached Head | cut -f2 | grep lessons | cut -f1-4 -d/ | uniq)
else
  echo 'process params'
  out="$1"
  # convert tag dmap:projects:project-m3 into lessons/dmap/projects/project-m3
fi

IFS=' '
while read -r line;do
  echo "Processing ${line}"
  SRC_DIR=$root/$line
  dir=$(echo ${line}| cut -f1 -d/)
  echo "Testing ${dir}"

  if [ ${dir} = 'lessons' ]; then
    LESSON=$(echo ${line}| cut -f4 -d/)
    echo "doing ${TODO} ${line} ${dir} ${LESSON}"
    #echo "${SRC_DIR}"
    # cd to the directory so tar only keeps relative path
    #     --exclude='*.ipynb' --exclude='*.gz' ${line} &> /tmp/log.txt
    cd "${root}"
    gtar --sort=name --owner=root:0 --group=root:0 --mtime='UTC 2021-01-01' \
         -cvf ${LESSON}.tar \
         --exclude='*.ipynb' --exclude='*.tar.gz' ${line} &> /tmp/log.txt
    gzip -n ${LESSON}.tar
    /bin/mv ${LESSON}.tar.gz ${SRC_DIR}
    ls -la ${SRC_DIR}/*.gz
    git add ${SRC_DIR}
    echo 'tar file added via git'
    echo 'be sure to git commit'

  else
    echo "skip ${line}"
  fi

done <<< "$out"

