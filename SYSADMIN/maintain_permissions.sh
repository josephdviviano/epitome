#! /bin/bash

# sets proper experiment permissions for /srv/MRI/WORKING
cd /srv/MRI/WORKING/
for EXP in `ls -d */`; do
    EXP="${EXP%?}"
    if [ ! ${EXP} = 'FREESURFER' ]; then
        GROUPNAME=`echo ${EXP} | tr '[:upper:]' '[:lower:]'`
        groupadd -f ${GROUPNAME}

        chown -R grandvizier ${EXP}
        chgrp -R ${GROUPNAME} ${EXP}
        chmod -R 770 ${EXP}

        for RUN in `ls -d ${EXP}/*/*/*/RUN??/`; do
            chmod -R 750 ${RUN}
        done
    fi

    if  [ ${EXP} = 'FREESURFER' ]; then
        chown -R grandvizier ${EXP}
        chgrp -R staff ${EXP}
        chmod -R 750 ${EXP}
    fi
done

# sets proper experiment permissions for /srv/MRI/RAW
cd /srv/MRI/RAW/
for EXP in `ls -d */`; do
    chown -R grandvizier ${EXP}
    chgrp -R staff ${EXP}
    chmod -R 740 ${EXP}
done

# sets proper experiment permissions for /srv/MRI/ANALYSIS
cd /srv/MRI/ANALYSIS/
for EXP in `ls -d */`; do
    chown -R grandvizier ${EXP}
    chgrp -R staff ${EXP}
    chmod -R 770 ${EXP}
done