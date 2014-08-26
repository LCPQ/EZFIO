#!/bin/bash

OLD_DIR=$PWD
cd ../.git/hooks/

for i in commit-msg post-commit
do
  rm $i
  ln -s $OLD_DIR/$i $PWD/$i
done
