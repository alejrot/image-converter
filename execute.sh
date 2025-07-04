#! /bin/bash

system=`uname`
system=${system,,}  # conversion to lowercase
if [ $system = "linux" ]  
then
    echo "Platform: GNU/Linux"
    program_folder=/opt/image-converter/
    cd $program_folder
    source .venv/bin/activate
else
    echo "Platform: Windows"
    program_folder="c:/Program Files/image-converter"
    cd $program_folder
    source .venv/Scripts/activate
fi


args=("$@")
python main.py ${args[*]}  

deactivate