for s in *; do 
    for f in `ls stim_onsets/*`; do
        file=`basename ${f}`
        cp ${f} ${s}/${file}
    done
    cd ${s}
    3dDeconvolve -input func_MNI.01.nii.gz func_MNI.02.nii.gz func_MNI.03.nii.gz func_MNI.04.nii.gz \
                 -mask anat_EPI_mask_MNI.nii.gz \
                 -polort 4 \
                 -num_stimts 12 \
                 -local_times \
                 -jobs 8 \
                 -x1D first_level_design.mat \
                 -stim_times 1 Music_Audio.txt 'BLOCK(12,1)' \
                 -stim_times 2 Music_AVAsync.txt 'BLOCK(12,1)' \
                 -stim_times 3 Music_AVSync.txt 'BLOCK(12,1)' \
                 -stim_times 4 Music_Visual.txt 'BLOCK(12,1)' \
                 -stim_times 5 SocLin_Audio.txt 'BLOCK(12,1)' \
                 -stim_times 6 SocLing_AVAsync.txt 'BLOCK(12,1)' \
                 -stim_times 7 SocLing_AVSync.txt 'BLOCK(12,1)' \
                 -stim_times 8 SocLing_Visual.txt 'BLOCK(12,1)' \
                 -stim_times 9 SocNonLing_Audio.txt 'BLOCK(12,1)' \
                 -stim_times 10 SocNonLing_AVAsync.txt 'BLOCK(12,1)' \
                 -stim_times 11 SocNonLing_AVSync.txt 'BLOCK(12,1)' \
                 -stim_times 12 SocNonLing_Visual.txt 'BLOCK(12,1)' \
                 -stim_label 1 music_a \
                 -stim_label 2 music_av_async \
                 -stim_label 3 music_av_sync \
                 -stim_label 4 music_v \
                 -stim_label 5 socling_a \
                 -stim_label 6 socling_av_async \
                 -stim_label 7 socling_av_sync \
                 -stim_label 8 socling_v \
                 -stim_label 9 socnonling_a \
                 -stim_label 10 socnonling_av_async \
                 -stim_label 11 socnonling_av_sync \
                 -stim_label 12 socnonling_v \
                 -ortvec motion_socling.1D motion_paramaters \
                 -num_glt 1 \
                 -glt_label 1 music-a_vs_music-v \
                 -gltsym 'SYM: +music_a -music_v' \
                 -fitts ts_explained.nii.gz \
                 -bucket first_level.nii.gz \
                 -cbucket first_level_coeffs.nii.gz \
                 -fout \
                 -tout \
                 -xjpeg glm_matrix.jpg
    cd ..
done