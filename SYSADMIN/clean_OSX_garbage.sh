# clean up OSX Junk

find . -name \.AppleDouble -exec rm -rf {} \;
find . -name \.DS_Store -exec rm -rf {} \;
find . -name \.AppleDB -exec rm -rf {} \;
find . -name \.AppleDesktop -exec rm -rf {} \;