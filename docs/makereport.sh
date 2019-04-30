#!/bin/bash
###variable
tpl="edubian.tpl"
export EDUBIANUSERPROFILE=${HOME}/Assignment/.${USER}


###Prepare
rm -rv ${HOME}/report
rm -v ${HOME}/${USER}.tar.gz

## Check template exist
if [ -f "$tpl" ]
then
	echo "Template $tpl found."
	echo "Remove it"
	rm -v ${PWD}/$tpl
	echo "Download from github..."
	## get template for converter
	wget https://raw.githubusercontent.com/kostyan6812/edubian/master/docs/edubian.tpl
else
	echo "Template $file not found."
	echo "Download from github..."
	## get template for converter
	wget https://raw.githubusercontent.com/kostyan6812/edubian/master/docs/edubian.tpl
fi


##prepare for report
cd ${HOME}
mkdir -v report

for file in Assignment/Topics/${USER}*.ipynb; do
	STR="$(grep -c "username ${USER}" $file)"
	 if [[ ${STR} == 0 ]]
	 then
	  echo ${file%.*}.html
	  sed -i '/User/ s/.$/\\n",/' $file
	  sed -i "/User/a\"username ${USER}\"" $file
	else
	  if [[ ${STR} == 1 ]]
	  then
	   echo "File has been prepared"
	  else
	   echo "Bad file. Terminate"
           exit 1
          fi
	fi
       jupyter-nbconvert $file --to html --template edubian
       mv ${file%.*}.html ${HOME}/report
done


## convert html to docx
for file in report/${USER}*.html; do
  pandoc $file --to=docx -o ${file%.*}.docx
  rm -vf $file 
done

## create archive
tar -czvf ${USER}.tar.gz report/

##clear
rm -rfv report
