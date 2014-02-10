for s in `ls -d *`; do \
    command='mkdir ~/Desktop/TRSE_RAW/'
    command=${command}${s}

    ssh -n jdv@130.63.40.171 `echo ${command}`;
    scp -r ${s}/SourceDICOMs/* jdv@130.63.40.171:~/Desktop/TRSE_RAW/${s};
done