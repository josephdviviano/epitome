#!/bin/bash

mkdir T1_OUT

directory=`pwd`
for d in *; do \
    subject=`basename ${d}`
    mkdir ${directory}/T1_OUT/${subject}
    for f in ${d}/MPRAGE*; do \
        file=`basename ${f}`
        Dimon -infile_prefix ${f}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
        mv *.nii ${directory}/T1_OUT/${subject}/${file}.nii.gz
        rm dimon.files.run*
        rm GERT_Reco_dicom*
    done
done

for d in *; do \
    subject=`basename ${d}`
    mkdir ${directory}/T1_OUT/${subject}
    for f in ${d}/mprage*; do \
        file=`basename ${f}`
        Dimon -infile_prefix ${f}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
        mv *.nii ${directory}/T1_OUT/${subject}/${file}.nii.gz
        rm dimon.files.run*
        rm GERT_Reco_dicom*
    done
done

1341
1341-2
1342
1342-2

cd 1341
mkdir NII_OUT
for d in TRSE_Block_*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
for d in MPRAGE*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
rm dimon*
rm GERT*
mv NII_OUT ../OUT_1341
cd ..

cd 1341-2
mkdir NII_OUT
for d in TRSE_Block_*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
for d in MPRAGE*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
rm dimon*
rm GERT*
mv NII_OUT ../OUT_1341-2
cd ..

cd 1342
mkdir NII_OUT
for d in TRSE_Block_*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
for d in MPRAGE*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
rm dimon*
rm GERT*
mv NII_OUT ../OUT_1342
cd ..

cd 1342-2
mkdir NII_OUT
for d in TRSE_Block_*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
for d in MPRAGE*; do
    Dimon -infile_prefix ${d}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
    gzip *.nii
    mv *.nii.gz NII_OUT/${d}.nii.gz
done
rm dimon*
rm GERT*
mv NII_OUT ../OUT_1342-2
cd ..


mv OUT_1342/TRSE_Block_01.nii.gz TASK/SESS01/RUN01/
mv OUT_1342/TRSE_Block_02.nii.gz TASK/SESS01/RUN02/
mv OUT_1342/TRSE_Block_03.nii.gz TASK/SESS01/RUN03/
mv OUT_1342/TRSE_Block_04.nii.gz TASK/SESS01/RUN04/
mv OUT_1342/TRSE_Block_05.nii.gz TASK/SESS01/RUN05/
mv OUT_1342/TRSE_Block_06.nii.gz TASK/SESS01/RUN06/
mv OUT_1342/TRSE_Block_07.nii.gz TASK/SESS01/RUN07/
mv OUT_1342/TRSE_Block_08.nii.gz TASK/SESS01/RUN08/
mv OUT_1342/TRSE_Block_09.nii.gz TASK/SESS01/RUN09/
mv OUT_1342/TRSE_Block_10.nii.gz TASK/SESS01/RUN10/
mv OUT_1342/TRSE_Block_11.nii.gz TASK/SESS01/RUN11/
mv OUT_1342/TRSE_Block_12.nii.gz TASK/SESS01/RUN12/
mv OUT_1342/TRSE_Block_13.nii.gz TASK/SESS01/RUN13/
mv OUT_1342/TRSE_Block_14.nii.gz TASK/SESS01/RUN14/
mv OUT_1342/TRSE_Block_15.nii.gz TASK/SESS01/RUN15/
mv OUT_1342/TRSE_Block_16.nii.gz TASK/SESS01/RUN16/
mv OUT_1342/TRSE_Block_17.nii.gz TASK/SESS01/RUN17/
mv OUT_1342/TRSE_Block_18.nii.gz TASK/SESS01/RUN18/
mv OUT_1342/TRSE_Block_19.nii.gz TASK/SESS01/RUN19/
mv OUT_1342/TRSE_Block_20.nii.gz TASK/SESS01/RUN20/


for d in *; do
    mkdir ${d}/RUN01
    mkdir ${d}/RUN02
    mkdir ${d}/RUN03
    mkdir ${d}/RUN04
    mkdir ${d}/RUN05
    mkdir ${d}/RUN06
    mkdir ${d}/RUN07
    mkdir ${d}/RUN08
    mkdir ${d}/RUN09
    mkdir ${d}/RUN10
    mkdir ${d}/RUN11
    mkdir ${d}/RUN12
    mkdir ${d}/RUN13
    mkdir ${d}/RUN14
    mkdir ${d}/RUN15
    mkdir ${d}/RUN16
    mkdir ${d}/RUN17
    mkdir ${d}/RUN18
    mkdir ${d}/RUN19
    mkdir ${d}/RUN20
done