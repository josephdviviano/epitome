#!/bin/tcsh -xef
#Purpose: Creates a correlation coefficient for each ROI's resting state signal and outputs the single value to a text file
# Authored by: C. Peng, 3/2013
# Use "REST" for all other methods, "LOC" for PEAK
# Use THRESHREF for all other methods, NO THRESHREF for PEAK

set contrast = $argv[1]
set space = $argv[2]
#set METHODS = $argv[3]

set subjects = (03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 28 29 30 31 32 34 35 36 37)
#set subjects = (03)
#set METHODS = (r6_tX r10_t0 r6_t0 r10_t2.58 r6_t2.58)
set METHODS = (r6_t2.58)

foreach subjnum($subjects)

	set ROIfile = /misc/data69/stevenswd/COP/DATA/FMRI/GROUP/RSFCMRI/ROIFILES/s{$subjnum}_lh_ROIs_{$contrast}.1D
	#for WORD-NENT
	#set ROIs = (L_VWFA L_FFA L_aFFA L_pFFA L_LOC L_PFs L_WERN L_BROC L_STG L_MTG L_PCG L_ANG)
	#for ANIMAL-TOOL ONLY
	#set ROIs = (L_mFG L_amFG L_pmFG R_mFG R_amFG R_pmFG L_latFG R_latFG L_pSTS R_pSTS L_EBA R_EBA L_AMG R_AMG R_IFJ L_pMTG R_pMTG L_vPM R_vPM L_IPL R_IPL L_IPS R_IPS)	
	#for ANIMAL-TOOL AND FACE-SCENE COMBINED
	set ROIs = (L_latFG R_latFG L_mFG L_pmFG L_amFG R_mFG R_pmFG R_amFG L_FFA L_pFFA L_aFFA R_FFA R_pFFA R_aFFA L_PPA R_PPA L_pSTS_A R_pSTS_A L_EBA R_EBA L_AMG_A R_AMG_A R_IFJ_A L_pMTG R_pMTG L_vPM R_vPM L_IPL R_IPL L_IPS R_IPS L_OFA R_OFA L_pSTS_F R_pSTS_F L_IFJ_F R_IFJ_F L_ATL R_ATL L_AMG_F R_AMG_F L_RSC R_RSC L_TOS R_TOS)


	set allROIs = ()
	set allROIs = ($allROIs $ROIs)

	foreach method($METHODS)
	
		cd /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/
		mkdir TEMP_PEARSON
		cd TEMP_PEARSON
		mkdir {$method}
		set output_pearson_dir = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/TEMP_PEARSON/{$method}/
		set rest_dir = /misc/data69/stevenswd/COP/DATA/FMRI/1*3TB*0{$subjnum}/ROI/VOL/{$contrast}/ROISIGNALS_REST/{$method}
		
		cd $rest_dir
	

foreach region1($allROIs)
	foreach region2($allROIs)
		if (-e RestSignal_s{$subjnum}_{$space}_{$contrast}_{$region1}_I{$method}.1D) then
			if (-e RestSignal_s{$subjnum}_{$space}_{$contrast}_{$region2}_I{$method}.1D) then
				if ($region1 == $region2) then
					echo 1 > Pearson_s{$subjnum}_{$region1}-{$region2}_{$contrast}_{$method}.txt
					mv Pearson_s{$subjnum}_{$region1}-{$region2}_{$contrast}_{$method}.txt $output_pearson_dir
				else
					1dCorrelate RestSignal_s{$subjnum}_{$space}_{$contrast}_{$region1}_I{$method}.1D RestSignal_s{$subjnum}_{$space}_{$contrast}_{$region2}_I{$method}.1D > temp.txt
					cat temp.txt | awk '{print $3}' > temp2.txt
					sed '4 p' -n temp2.txt > Pearson_s{$subjnum}_{$region1}-{$region2}_{$contrast}_{$method}.txt
					rm temp.txt
					rm temp2.txt
					mv Pearson_s{$subjnum}_{$region1}-{$region2}_{$contrast}_{$method}.txt $output_pearson_dir
					cd $rest_dir
				endif
			else
				echo $region2 " RESTSIGNAL DOES NOT EXIST. TRY AGAIN LATER."	
			endif
		else
			echo $region1 " RESTSIGNAL DOES NOT EXIST. TRY AGAIN LATER."
		endif
	end	#region2
end #region1

	end #end of methods loop
	
end #end of subjects loop
