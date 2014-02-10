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
