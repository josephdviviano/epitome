# read dicom header - return subject identifier (siemens specific header)
for d in *; do ssid=`cat ${d}/*-1.dcm | sed -n 2p | cut -c 600-1000 | grep -oa ......_4TT.....`; echo 'directory ' ${d} ' subject ' ${ssid}; done > directory_subject.txt


