#  Remove default installation folder
echo "Uninstalling program"

system=`uname`
system=${system,,}  # conversion to lowercase
if [ $system = "linux" ]  
then
    echo "Platform: GNU/Linux"
    program_folder=/opt/image-converter/
    rm -r $program_folder
else
    echo "Platform: Windows"
    program_folder="c:/Program Files/image-converter"
    rm -r $program_folder

fi



echo "Done!"