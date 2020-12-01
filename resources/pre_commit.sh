#!/usr/local/bin/zsh
#!/bin/bash
# get all the files that are ready to commit
# user has executed git add . 

root="/Users/mikeh/home/projects/CodeStoryLessons"
out=$(git diff-index --cached Head | cut -f2 | grep lessons | cut -f1-4 -d/ | uniq)
for i in $out; do
  # lessons/dmap/projects/project-m3
  SRC_DIR=$root/$i
  dir=$(echo ${i}| cut -f1 -d/)
  if [ ${dir} = 'lessons' ]; then
    LESSON=$(echo ${i}| cut -f4 -d/)
    echo "doing ${TODO} ${i} ${dir} ${LESSON}"
    #echo "${SRC_DIR}"
    # cd to the directory so tar only keeps relative path
    cd "${root}"
    gtar --sort=name --owner=root:0 --group=root:0 --mtime='UTC 2021-01-01' -cvf ${LESSON}.tar --exclude='*.ipynb' --exclude='*.gz' ${i} &> /tmp/log.txt
    gzip -n ${LESSON}.tar
    /bin/mv ${LESSON}.tar.gz ${SRC_DIR}
    echo 'created'
    ls -la ${SRC_DIR}/*.gz
    git add ${SRC_DIR}
    echo 'tar file added via git'
    echo 'be sure to git commit'

  else
    echo "skip ${i}"
  fi
done
