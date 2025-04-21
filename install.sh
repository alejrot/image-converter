#! /bin/bash

echo "Installing program"

#  Choose default installation folder
system=`uname`
system=${system,,}  # conversion to lowercase
if [ $system = "linux" ]  
then
    echo "Platform: GNU/Linux"
    program_folder=/opt/image-converter/
else
    echo "Platform: Windows"
    program_folder="c:/Program Files/image-converter"
fi

# Create installation folder if it doesn't exists
if [ -d $program_folder ]
then
    echo "Installation folder exists already"
else
    echo "Creating installation folder"
    mkdir $program_folder
fi

# copy source code
cp main.py requirements.txt  $program_folder
cp -r  code/ locale/  $program_folder
cp  install.sh execute.sh compile.sh ./uninstall.sh $program_folder


# create a virtual environment
cd $program_folder
python -m venv .venv

if [ $system = "linux" ]  
then
    # GNU/Linux
    source .venv/bin/activate
else
    # Windows
    source .venv/Scripts/activate
fi

# install all necessary packages in virtual environment
pip install -r requirements.txt 
pip install --upgrade pip


chmod +x ./execute.sh ./uninstall.sh


echo "Done!"