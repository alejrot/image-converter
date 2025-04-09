#! /bin/bash

system=`uname`
system=${system,,}  # conversion to lowercase
if [ $system = "linux" ]  
then
    echo "Platform: GNU/Linux"
    source .venv/bin/activate
else
    echo "Platform: Windows"
    source .venv/Scripts/activate
fi


args=("$@")
python main.py ${args[*]}  

deactivate