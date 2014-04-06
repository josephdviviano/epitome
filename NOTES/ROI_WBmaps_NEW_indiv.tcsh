#!/bin/tcsh -xef
#PURPOSE: Whole Brain correlation maps between a given ROI and rest scan
#USAGE: for Individual ROIs in any space. Do not use for TLRC!
#NEEDS: ROIs in their properly named methods folder, Rest scan in A/PROC folder, 1D files under ROISIGNALS_REST folder
#Authored by C. Peng, 3/2013
#FOR INDIVIDUAL ROIS

set contrast = $argv[1]
set space = $argv[2]

#FOR WORD-NENT
	set SEEDROIS = (L_VWFA L_aFFA L_pFFA L_FFA L_LOC L_PFs)
#FOR COMBINED ANIMAL-TOOL AND FACE-SCENE
#set SEEDROIS = (L_mFG L_amFG L_pmFG L_latFG L_FFA L_pFFA L_aFFA L_PPA R_mFG R_amFG R_pmFG R_latFG R_FFA R_pFFA R_aFFA R_PPA)


#set subjects = (03 04 05 06 07 08 09 10 11 12 14 15 16 17 18 19 20 21 22 23 24 25 26 28 29 30 31 32 34 35 36 37)
set subjects = (36)

set METHODS = (r10_t0 r6_t0 r10_t2.58 r6_t2.58 r6_tX)
#set METHODS = (PEAK)

#Make the 1D file correlation between a given ROI and the rest file

foreach subjnum($subjects)

		set ROIfile = /misc/data69/stevenswd/COP/DATA/FMRI/GROUP/RSFCMRI/ROIFILES/s{$subjnum}_lh_ROIs_{$contrast}.1D

	foreach method($METHODS)

			if ($subjnum == 24) then
				set run = 03
			else
				set run = 01
			endif

		#set masks_dir = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/{$space}/{$method}
		set signals_dir = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/ROISIGNALS_REST/{$method}
		set restPath = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*{$subjnum}/A/PROC/REST_RESULTS
		set restFile = {$restPath}/s{$subjnum}.REST{$run}.clean_DVe.blur6IV.scaled+orig.HEAD

		cd /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/
		mkdir WB_MAPS
		cd WB_MAPS
		mkdir {$method}

		set output_dir = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/WB_MAPS/{$method}

		cd {$output_dir}

			foreach roi($SEEDROIS)

				3dTcorr1D -pearson -float -prefix Tcorr1D_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method} \
						{$restFile} {$signals_dir}/RestSignal_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method}.1D
				3dcalc -a Tcorr1D_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method}+orig. \
					-expr 'atanh(a)' -prefix Tcorr1D_z_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method}
				rm Tcorr1D_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method}+orig.BRIK
				rm Tcorr1D_s{$subjnum}_{$space}_{$contrast}_{$roi}_{$method}+orig.HEAD

		end #end of ROI loop

	end #end of methods loop

end #end of subjects loop
