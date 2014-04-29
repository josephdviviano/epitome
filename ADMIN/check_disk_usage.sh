#!/bin/bash

# checks disk usage for all users

for user in *;
do
echo "Checking Tiered Storage for "$user""

echo "Archive"
sudo du -hs "$user"/archive

echo "Current"
sudo du -hs "$user"/current

echo "Scratch"
sudo du -hs "$user"/scratch

done
