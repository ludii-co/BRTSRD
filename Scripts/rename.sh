#!/bin/bash
n=1000
for f in *
do
  if [ "$f" = "rename.sh" ]
  then
    continue
  fi
  mv "$f" "$((n++)).png"
done

n=1
for f in *
do
  if [ "$f" = "rename.sh" ]
  then
    continue
  fi
  mv "$f" "$((n++)).png"
done