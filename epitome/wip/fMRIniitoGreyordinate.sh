#!/bin/bash 
set -e

# Requirements for this script
#  installed versions of: FSL (version 5.0.6), FreeSurfer (version 5.3.0-HCP) , gradunwarp (HCP version 1.0.2)
#  environment: use SetUpHCPPipeline.sh  (or individually set FSLDIR, FREESURFER_HOME, HCPPIPEDIR, PATH - for gradient_unwarp.py)


# --------------------------------------------------------------------------------
#  Load Function Libraries
# --------------------------------------------------------------------------------
#EnvironmentScript="${HOME}/Documents/lerch/spatnav_rest/scripts/SetUpHCPPipeline_mac.sh" #Pipeline environment script
EnvironmentScript="/home/j/jlerch/edickie/myscripts/fMRI/spatnav_rest/SetUpHCPPipeline_scinet.sh" #Pipeline environment script scinet path

source $EnvironmentScript

source $HCPPIPEDIR/global/scripts/log.shlib  # Logging related functions
source $HCPPIPEDIR/global/scripts/opts.shlib # Command line option functions

################################################ SUPPORT FUNCTIONS ##################################################

# --------------------------------------------------------------------------------
#  Usage Description Function
# --------------------------------------------------------------------------------

show_usage() {
    echo "Usage information To Be Written"
    exit 1
}

# --------------------------------------------------------------------------------
#   Establish tool name for logging
# --------------------------------------------------------------------------------
log_SetToolName "fMRIniitoGreyordinate.sh"

################################################## OPTION PARSING #####################################################

opts_ShowVersionIfRequested $@

if opts_CheckForHelpRequest $@; then
    show_usage
fi

log_Msg "Parsing Command Line Options"

# parse arguments
Path=`opts_GetOpt1 "--path" $@`  # "$1"
Subject=`opts_GetOpt1 "--subject" $@`  # "$2"
SmoothingFWHM=`opts_GetOpt1 "--smoothingFWHM" $@`  # "${3}"

if [ "${RegName}" = "" ]; then
    RegName="FS"
fi

RUN=`opts_GetOpt1 "--printcom" $@`  # use ="echo" for just printing everything and not running the commands (default is to run)

log_Msg "Path: ${Path}"
log_Msg "Subject: ${Subject}"
log_Msg "SmoothingFWHM: ${SmoothingFWHM}"
log_Msg "RUN: ${RUN}"

# Setup PATHS
PipelineScripts=${HCPPIPEDIR_fMRISurf}
HCPFolder="$Path"/"hcp"
FSFolder="$Path"/"FSout"
FeatFolder="$Path"/"featprep"

#Templates and settings
AtlasSpaceFolder="$HCPFolder"/"$Subject"/MNINonLinear
AtlasTransform="$AtlasSpaceFolder"/xfms/acpc2standard_warp
DownSampleFolder="$AtlasSpaceFolder"/"fsaverage_LR32k"
FinalfMRIResolution="2"
GrayordinatesResolution="2"
InverseAtlasTransform="$AtlasSpaceFolder"/xfms/standard2acpc
LowResMesh="32"
NameOffMRI="RSN"
NativeFolder="Native"
OutputAtlasDenseTimeseries="${NameOffMRI}_Atlas"
RegName="FS"
ResultsFolder="$AtlasSpaceFolder"/Results/"$NameOffMRI"
ROIFolder="$AtlasSpaceFolder"/ROIs
StandardSpacefMRI=${FeatFolder}/${Subject}.feat/reg_standard/filtered_func_data_clean2
StandardSpaceMeanImage=${FeatFolder}/${Subject}.feat/reg/example_func2standard

###### from end of volume mapping pipeline

log_Msg "mkdir -p ${ResultsFolder}"
mkdir -p ${ResultsFolder}
cp -r ${StandardSpacefMRI}.nii.gz ${ResultsFolder}/${NameOffMRI}.nii.gz
cp -r ${StandardSpaceMeanImage}.nii.gz ${ResultsFolder}/${NameOffMRI}_SBRef.nii.gz


#Make fMRI Ribbon
#Noisy Voxel Outlier Exclusion
#Ribbon-based Volume to Surface mapping and resampling to standard surface

log_Msg "Make fMRI Ribbon"
log_Msg "mkdir -p ${ResultsFolder}/RibbonVolumeToSurfaceMapping"
mkdir -p "$ResultsFolder"/RibbonVolumeToSurfaceMapping
"$PipelineScripts"/RibbonVolumeToSurfaceMapping.sh \
	"$ResultsFolder"/RibbonVolumeToSurfaceMapping \
	"$ResultsFolder"/"$NameOffMRI" \
	"$Subject" \
	"$DownSampleFolder" \
	"$LowResMesh" \
	"$AtlasSpaceFolder"/"$NativeFolder" \
	"${RegName}"


#Surface Smoothing
log_Msg "Surface Smoothing"
"$HCPPIPEDIR_fMRISurf"/SurfaceSmoothing.sh \
	"$ResultsFolder"/"$NameOffMRI" \
	"$Subject" \
	"$DownSampleFolder" \
	"$LowResMesh" \
	"$SmoothingFWHM"

#Subcortical Processing
log_Msg "Subcortical Processing"
"$HCPPIPEDIR_fMRISurf"/SubcorticalProcessing.sh \
	"$AtlasSpaceFolder" \
	"$ROIFolder" \
	"$FinalfMRIResolution" \
	"$ResultsFolder" \
	"$NameOffMRI" \
	"$SmoothingFWHM" \
	"$GrayordinatesResolution"

#Generation of Dense Timeseries
log_Msg "Generation of Dense Timeseries"
"$PipelineScripts"/CreateDenseTimeseries.sh \
	"$DownSampleFolder" \
	"$Subject" \
	"$LowResMesh" \
	"$ResultsFolder"/"$NameOffMRI" \
	"$SmoothingFWHM" \
	"$ROIFolder" \
	"$ResultsFolder"/"$OutputAtlasDenseTimeseries" \
	"$GrayordinatesResolution"

# Dilation step for cortical surface glm - dunno if this is really needed..but it's in the hcp pipeline
log_Msg "Cortical Surface Dilation"
for Hemisphere in L R ; do
  #Prepare for film_gls
  ${CARET7DIR}/wb_command -metric-dilate "$ResultsFolder"/"$NameOffMRI"_s"$SmoothingFWHM".atlasroi."$Hemisphere"."$LowResMesh"k_fs_LR.func.gii "$DownSampleFolder"/"$Subject"."$Hemisphere".midthickness."$LowResMesh"k_fs_LR.surf.gii 50 "$ResultsFolder"/"$NameOffMRI"_s"$SmoothingFWHM".atlasroi_dil."$Hemisphere"."$LowResMesh"k_fs_LR.func.gii -nearest
done

log_Msg "Completed"
