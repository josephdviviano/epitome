#! /bin/bash
#IN_PRE='def_D'
#IN_PRE='def_F'
#IN_PRE='d_attn_C'
#IN_PRE='ATOL_MPFC'
#IN_PRE='ATOL_PCC'

CMD1=`echo '"'group1/*${IN_PRE}.nii.gz[1]'"'`

# group - level maps
3dttest++ \
    -setA "group1/*ATOL_PCC.nii.gz[1]" \
    -setB 'group2/*ATOL_PCC.nii.gz[1]' \
    -labelA young \
    -labelB old \
    -BminusA \
    -prefix group_analysis_ATOL_PCC.nii.gz \
    -pooled\
    -mask brain_mask.nii.gz