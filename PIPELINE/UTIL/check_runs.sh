# test that all runs have the expected number of TRs
echo 'Generating 4D file dimensions for '${DIR_EXPT}
echo Subj_ID,Session,Run,X,Y,Z,TR > ${DIR_DATA}/${DIR_EXPT}/EPI_overview.csv
for SUB in ${SUBJECTS}; do
    DIR_SESS=`ls -d -- ${DIR_DATA}/${DIR_EXPT}/${SUB}/${DATA_TYPE}/*/`
    for SESS in ${DIR_SESS}; do
        DIR_RUNS=`ls -d -- ${SESS}/RUN*`
        for RUN in ${DIR_RUNS}; do
            NUM=`basename ${RUN} | sed 's/[^0-9]//g'`
            FILE=`echo ${RUN}/*.nii.gz`

            # grab the number of TRs
            X=`fslhd ${FILE} | sed -n 6p | cut -c 5- | xargs`
            Y=`fslhd ${FILE} | sed -n 7p | cut -c 5- | xargs`
            Z=`fslhd ${FILE} | sed -n 8p | cut -c 5- | xargs`
            TR=`fslhd ${FILE} | sed -n 9p | cut -c 5- | xargs`
            echo `basename ${SUB}`,`basename ${SESS}`,`basename ${RUN}`,${X},${Y},${Z},${TR} >> ${DIR_DATA}/${DIR_EXPT}/EPI_overview.csv

        done
    done
done
echo 'Wrote data to '${DIR_DATA}/${DIR_EXPT}/EPI_overview.csv

# JDV Mar 14 2014