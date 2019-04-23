#!/bin/bash

## get template for converter
wget https://raw.githubusercontent.com/kostyan6812/edubian/master/docs/edubian.tpl

##prepare for report
cd ${HOME}
mkdir -v report || echo 'dir exist, skip'

export EDUBIANUSERPROFILE=${HOME}/Assignment/.${USER}

## convert notebook to htm
for file in Assignment/Topics/*.ipynb; do
  echo ${file%.*}.html
  sed -i '/User/ s/.$/\\n",/' $file
  sed -i "/User/a\"username ${USER}\"" $file
  jupyter-nbconvert $file --to html --template edubian
  mv ${file%.*}.html ${HOME}/report
done

## convert html to docx
for file in report/*.html; do
  pandoc $file --to=docx -o ${file%.*}.docx
  rm -vf $file 
done

## create archive
tar -czvf ${USER}.tar.gz report/

##clear
rm -rfv report
