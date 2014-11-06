#!/bin/bash

# download the data into tmp/
echo '*** Grabbing data from AFNI ***'
mkdir tmp 
cd tmp
wget -c http://afni.nimh.nih.gov/sscc/staff/glend/matlab_compiler/McRetroTS_linux64pkg.zip
unzip McRetroTS_linux64pkg.zip

# run the installer
sudo ./MCRInstaller.bin

# remove temporary files
echo '*** Cleaning up ***'
cd ../
rm -r tmp

