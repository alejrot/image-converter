#! /bin/bash

python -m venv .venv

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


pip install -r requirements.txt 
pip install --upgrade pip