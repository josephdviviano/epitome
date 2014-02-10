#!/bin/bash

mkdir DICOM_OUT
directory=`pwd`
for d in *; do \
    subject=`basename ${d}`
    mkdir ${directory}/DICOM_OUT/${subject}
    for f in ${d}/SourceDICOMs/*; do \
        file=`basename ${f}`
        Dimon -infile_prefix ${f}/IM -gert_create_dataset -gert_write_as_nifti -dicom_org
        mv *.nii ${directory}/DICOM_OUT/${subject}/${file}.nii.gz
        rm dimon.files.run*
        rm GERT_Reco_dicom*
    done
done
