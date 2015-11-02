#!/usr/bin/python

import sys
import os.path
import subprocess

def docmd( list ):
   "This prints the command then runs it, takes in list"
   print "\n" + ' '.join(list)
   subprocess.call(list)
   return

# decides on which subject to process using number inputted
subid = str(sys.argv[1])
comp = str(sys.argv[2])

numComp = 10

#### SciNet paths
ica_dir='/scratch/j/jlerch/edickie/spatnav_rest/groupica/func_hipstr_sm0_n116_d10.ica/'
fsftemplate = '/home/j/jlerch/edickie/myscripts/fMRI/spatnav_rest/glm_icacomp.fsf'
filelist = '/home/j/jlerch/edickie/myscripts/fMRI/spatnav_rest/ica/filelist_func_hipstr_sm0_n116.txt'
project_dir = '/scratch/j/jlerch/edickie/spatnav_rest/'
standardbrain = '/home/j/jlerch/edickie/fsl/fsl5//data/standard/MNI152_T1_2mm_brain'
subjects_dir = project_dir + '/input/'
#####

# ## Macbook paths
# ica_dir='/Users/edickie/Documents/lerch/spatnav_rest/groupica/func_hipstr_sm0_mvqc_d10.ica/'
# fsftemplate = '/Users/edickie/Documents/lerch/spatnav_rest/scripts/glm_icacomp.fsf'
# filelist = '/Users/edickie/Documents/lerch/spatnav_rest/scripts/filelist_func_hipstr_sm0_mvqc.txt'
# standardbrain = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain'
# project_dir = '/Users/edickie/Documents/lerch/spatnav_rest/input_10_testing/'
# subjects_dir = project_dir + '/input_10/'
# ###


####other inputs - hard coded here for posterity
hcppath = project_dir + '/hcp/'
featin_dir = project_dir + '/featprep/'
outdir = project_dir + '/hcpglm_ica10_n116/' + subid ##actually the output dir
##note I changed this from volume ana - using none smooth data we get timeseries - in volume I extracted timeseries and modeled using 6mm smoothed data
ts_nii_in = featin_dir + '/' + subid + '.feat/reg_standard/filtered_func_data_clean2'
smoothingFWHM = '6'
func_folder = hcppath + subid +  '/MNINonLinear/Results/RSN/'
subcortical_nii_in = func_folder + 'RSN_AtlasSubcortical_s' + smoothingFWHM + '.nii.gz'
func_filepre = 	'RSN_s' + smoothingFWHM + '.atlasroi.'
func_fileext = 	'.32k_fs_LR.func.gii'
surf_folder= hcppath + '/' + subid + '/MNINonLinear/fsaverage_LR32k/'
surf_fileext = '.midthickness.32k_fs_LR.surf.gii'

### dilates the fMRI surfaces - dunno is this is important, but it's in the hcp pipeline
funcL_dil_gii=func_folder + func_filepre + '_dil.L' + func_fileext
if os.path.isfile(funcL_dil_gii) is False:
	for hemi in (["L","R"]):
		surf_gii = surf_folder + subid + '.' + hemi + surf_fileext
		hemi_in = func_folder + func_filepre + hemi + func_fileext
		func_dil_gii=func_folder + func_filepre + '_dil.' + hemi + func_fileext
		#dilate - dunno if this really matters
		docmd(['wb_command', '-metric-dilate',  hemi_in,
				surf_gii, '50', func_dil_gii, '-nearest'])


## cut the first 4 volumes from motion confounder
motion120 = subjects_dir + '/' + subid + '/' + subid + '_BOLDRSN_motionout.txt'
motion116 = subjects_dir + '/' + subid + '/' + subid + '_BOLDRSN_motionout116.txt'
## already done during volumetric analysis
if os.path.isfile(motion116) is False:
	with open(motion116, 'w') as m116:
		subprocess.Popen(['tail', '-n', "116", motion120], stdout=m116)

## make the outdir
docmd(['mkdir','-p', outdir])

## make output directory
comp_str = str(comp).zfill(2)
icatmpdir = outdir + '/ica' + comp_str
docmd(['mkdir','-p',icatmpdir])

## get weighted mean timeseries for the ICA component from the volume using the component probability map
compfileout = icatmpdir + '/meants_' + subid + '_' + comp_str +  '.txt'
docmd(['fslmeants',
	 '-i', ts_nii_in,
	 '-o', compfileout,
	 '-w', '-m', ica_dir + '/stats/probmap_'  + str(comp)])

## make design.fsf
design = icatmpdir + '/' + subid + '_ica' + comp_str

results_dir = icatmpdir + '/stats/'

#### make the feat design.fsf file for preprossing from template and run it
f1 = open(fsftemplate, 'r')
f2 = open(design + '.fsf', 'w')
for line in f1:
	line2 = line.replace('<STANDARDBRAIN>', standardbrain)
	line2 = line2.replace('<FEATIN>', subcortical_nii_in)
	line2 = line2.replace('<FEATDIROUT>', results_dir )
	line2 = line2.replace('<EV1_FILE>', compfileout )
	line2 = line2.replace('<EV1_NAME>', 'ica' + comp_str)
	line2 = line2.replace('<MOTION_CONFOUNDS>',	motion116)
	f2.write(line2)
f1.close()
f2.close()

## run feat model from the design.fsf
docmd(['feat_model', design, motion116])

## run feat glm on subcortical
results_sub_dir = icatmpdir + '/stats_subcortical/'
docmd(['film_gls',
	'--in=' + subcortical_nii_in,
	'--rn=' + results_sub_dir,
	'--pd=' + design + '.mat',
	'--thr=1', '--sa', '--ms=5',
	'--con=' + design + '.con'])

for hemi in (["L","R"]):
	results_dir = icatmpdir + '/stats_' + hemi + 'cortex/'
	func_dil_gii=func_folder + func_filepre + '_dil.' + hemi + func_fileext
	surf_gii = surf_folder + subid + '.' + hemi + surf_fileext
	docmd(['film_gls', '--rn=' + results_dir,
		'--sa', '--ms=15', '--epith=5',
		'--in2=' + surf_gii,
		'--in=' + func_dil_gii,
		'--pd=' + design + '.mat',
		'--con=' + design + '.con',
		'--mode=surface'])

## make a dense timeseries of the cope1 and cope1 z-stat (all I'm really interested in for the next step)
for statfile in ['cope1', 'zstat1']:
	docmd(['wb_command', '-cifti-create-dense-timeseries',
		icatmpdir + '/' + statfile + '.dtseries.nii',
		'-volume', icatmpdir + '/stats_subcortical/' + statfile + '.nii.gz',
		hcppath + subid + '/MNINonLinear/ROIs/Atlas_ROIs.2.nii.gz',
		'-left-metric', icatmpdir + '/stats_Lcortex/'  + statfile + '.func.gii',
		'-roi-left', surf_folder + '/' + subid + '.L.atlasroi.32k_fs_LR.shape.gii',
		'-right-metric', icatmpdir + '/stats_Rcortex/'  + statfile + '.func.gii',
		'-roi-right', surf_folder + '/' + subid +'.R.atlasroi.32k_fs_LR.shape.gii' ])
