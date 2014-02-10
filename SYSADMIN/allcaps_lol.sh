for s in *; do mv ${s}/task ${s}/TASK; 
               mv ${s}/behav ${s}/BEHAV;
               mv ${s}/physio ${s}/PHYSIO;
               mv ${s}/rest ${s}/REST;
               mv ${s}/t1 ${s}/T1;
               mv ${s}/localizer ${s}/LOCALIZER;
               mv ${s}/REST/sess01 ${s}/REST/SESS01; 
               mv ${s}/T1/sess01 ${s}/T1/SESS01;
               mv ${s}/T1/sess02 ${s}/T1/SESS02; 
               mv ${s}/TASK/sess01 ${s}/TASK/SESS01;
               mv ${s}/TASK/sess02 ${s}/TASK/SESS02; 
               mv ${s}/BEHAV/sess01 ${s}/BEHAV/SESS01;
               mv ${s}/PHYSIO/sess01 ${s}/PHYSIO/SESS01
               mv ${s}/LOCALIZER/sess01 ${s}/LOCALIZER/SESS01;
               mv ${s}/LOCALIZER/sess02 ${s}/LOCALIZER/SESS02;
               mv ${s}/REST/SESS01/run01 ${s}/REST/SESS01/RUN01;
               mv ${s}/REST/SESS01/run02 ${s}/REST/SESS01/RUN02; 
               mv ${s}/T1/SESS01/run01 ${s}/T1/SESS01/RUN01;
               mv ${s}/T1/SESS01/run02 ${s}/T1/SESS01/RUN02;
               mv ${s}/T1/SESS01/run03 ${s}/T1/SESS01/RUN03;
               mv ${s}/T1/SESS01/run04 ${s}/T1/SESS01/RUN04;
               mv ${s}/T1/SESS02/run01 ${s}/T1/SESS02/RUN01;
               mv ${s}/T1/SESS02/run02 ${s}/T1/SESS02/RUN02;
               mv ${s}/T1/SESS02/run03 ${s}/T1/SESS02/RUN03;
               mv ${s}/T1/SESS02/run04 ${s}/T1/SESS02/RUN04;
               mv ${s}/TASK/SESS01/run01/ ${s}/TASK/SESS01/RUN01/;
               mv ${s}/TASK/SESS01/run02/ ${s}/TASK/SESS01/RUN02/;
               mv ${s}/TASK/SESS01/run03/ ${s}/TASK/SESS01/RUN03/;
               mv ${s}/TASK/SESS01/run04/ ${s}/TASK/SESS01/RUN04/;
               mv ${s}/TASK/SESS01/run05/ ${s}/TASK/SESS01/RUN05/;
               mv ${s}/TASK/SESS01/run06/ ${s}/TASK/SESS01/RUN06/;
               mv ${s}/TASK/SESS01/run07/ ${s}/TASK/SESS01/RUN07/;
               mv ${s}/TASK/SESS01/run08/ ${s}/TASK/SESS01/RUN08/;
               mv ${s}/TASK/SESS01/run09/ ${s}/TASK/SESS01/RUN09/;
               mv ${s}/TASK/SESS01/run10/ ${s}/TASK/SESS01/RUN10/;
               mv ${s}/TASK/SESS01/run11/ ${s}/TASK/SESS01/RUN11/;
               mv ${s}/TASK/SESS01/run12/ ${s}/TASK/SESS01/RUN12/;
               mv ${s}/TASK/SESS01/run13/ ${s}/TASK/SESS01/RUN13/;
               mv ${s}/TASK/SESS01/run14/ ${s}/TASK/SESS01/RUN14/;
               mv ${s}/TASK/SESS01/run15/ ${s}/TASK/SESS01/RUN15/;
               mv ${s}/TASK/SESS01/run16/ ${s}/TASK/SESS01/RUN16/;
               mv ${s}/TASK/SESS01/run17/ ${s}/TASK/SESS01/RUN17/;
               mv ${s}/TASK/SESS01/run18/ ${s}/TASK/SESS01/RUN18/;
               mv ${s}/TASK/SESS01/run19/ ${s}/TASK/SESS01/RUN19/;
               mv ${s}/TASK/SESS01/run20/ ${s}/TASK/SESS01/RUN20/;
               mv ${s}/TASK/SESS01/params/ ${s}/TASK/SESS01/PARAMS/;
               mv ${s}/TASK/SESS02/run01/ ${s}/TASK/SESS02/RUN01/;
               mv ${s}/TASK/SESS02/run02/ ${s}/TASK/SESS02/RUN02/;
               mv ${s}/TASK/SESS02/run03/ ${s}/TASK/SESS02/RUN03/;
               mv ${s}/TASK/SESS02/run04/ ${s}/TASK/SESS02/RUN04/;
               mv ${s}/TASK/SESS02/run05/ ${s}/TASK/SESS02/RUN05/;
               mv ${s}/TASK/SESS02/run06/ ${s}/TASK/SESS02/RUN06/;
               mv ${s}/TASK/SESS02/run07/ ${s}/TASK/SESS02/RUN07/;
               mv ${s}/TASK/SESS02/run08/ ${s}/TASK/SESS02/RUN08/;
               mv ${s}/TASK/SESS02/run09/ ${s}/TASK/SESS02/RUN09/;
               mv ${s}/TASK/SESS02/run10/ ${s}/TASK/SESS02/RUN10/;
               mv ${s}/TASK/SESS02/run11/ ${s}/TASK/SESS02/RUN11/;
               mv ${s}/TASK/SESS02/run12/ ${s}/TASK/SESS02/RUN12/;
               mv ${s}/TASK/SESS02/run13/ ${s}/TASK/SESS02/RUN13/;
               mv ${s}/TASK/SESS02/run14/ ${s}/TASK/SESS02/RUN14/;
               mv ${s}/TASK/SESS02/run15/ ${s}/TASK/SESS02/RUN15/;
               mv ${s}/TASK/SESS02/run16/ ${s}/TASK/SESS02/RUN16/;
               mv ${s}/TASK/SESS02/run17/ ${s}/TASK/SESS02/RUN17/;
               mv ${s}/TASK/SESS02/run18/ ${s}/TASK/SESS02/RUN18/;
               mv ${s}/TASK/SESS02/run19/ ${s}/TASK/SESS02/RUN19/;
               mv ${s}/TASK/SESS02/run20/ ${s}/TASK/SESS02/RUN20/;
               mv ${s}/TASK/SESS02/params/ ${s}/TASK/SESS02/PARAMS/;
               mv ${s}/PHYSIO/SESS01/run01 mv ${s}/PHYSIO/SESS01/RUN01;
            done


for s in *; do mkdir ${s}/LOCALIZER/SESS01/RUN01;
               mkdir ${s}/LOCALIZER/SESS01/RUN02;
               mv ${s}/LOCALIZER/SESS01/Functional_Localizer.nii.gz ${s}/LOCALIZER/SESS01/RUN01/Functional_Localizer.nii.gz
               mv ${s}/LOCALIZER/SESS01/Functional_Localizer_2.nii.gz ${s}/LOCALIZER/SESS01/RUN02/Functional_Localizer_2.nii.gz
               mkdir ${s}/LOCALIZER/SESS02/RUN01;
               mkdir ${s}/LOCALIZER/SESS02/RUN02;
               mv ${s}/LOCALIZER/SESS02/Functional_Localizer.nii.gz ${s}/LOCALIZER/SESS02/RUN01/Functional_Localizer.nii.gz
               mv ${s}/LOCALIZER/SESS02/Functional_Localizer_2.nii.gz ${s}/LOCALIZER/SESS02/RUN02/Functional_Localizer_2.nii.gz
            done


