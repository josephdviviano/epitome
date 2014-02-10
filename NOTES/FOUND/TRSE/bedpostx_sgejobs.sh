export FSLDIR=/usr/local/fsl-4.1.4
. ${FSLDIR}/etc/fslconf/fsl.sh
export PATH=${FSLDIR}/bin:${PATH}:/usr/local/sge-6.2/bin/lx24-x86/
$FSLDIR/bin/bedpostx /home/despo/enhance/MRIdata_subjects/TRSE/1210-2/Despo/DTI/Dtifit 2 1 1000

