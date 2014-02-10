#!/bin/bash



to_afni="n"
slice_timing_corr="n"
rigid_mot_corr="n"
talaraich="n"



##################### slice-timing correction ######################
# Written by Marina Mandic, edited by Wayne Khuu
###################################################################

if [ $slice_timing_corr = "y" ]; then
cd $save_directory
    num_of_runs=0
    comb_code=""
    while [ $num_of_runs -lt $num_runs ]
      do
      num_of_runs=`expr $num_of_runs + 1`
      echo "Realignment for run"$num_of_runs
      3dTshift -verbose -prefix PTrun$num_of_runs -slice 1 -Fourier Prun$num_of_runs"+orig"
      comb_code=$comb_code"PTrun"$num_of_runs"+orig "
    done
    3dTcat -rlt+ -prefix all_PTruns $comb_code 
#fi 

######################################## Rigid motion correction ########################################################################################
# Note: this program finds a TR that has an overall minimum distance from the average of each motion parameter, then realigns all other TR's to this TR.# 
#########################################################################################################################################################

if [ $rigid_mot_corr = "y" ]; then
cd $save_directory
echo Rigid Motion Correction

# Broad correction, create 1D file which will be used for analysis
echo creating 1D file for analysis 
3dvolreg -prefix testing -base "run1+orig[20]" -zpad 2 -twopass -twodup -Fourier -1Dfile testing.1D -dfile testing1dfile all_PTruns+orig

echo READING 1D FILE
echo roll pitch yaw dS dL dP

run=0
x=0

min[1]=999999
min[2]=999999
min[3]=999999
min[4]=999999
min[5]=999999
min[6]=999999

max[1]=-999999
max[2]=-999999
max[3]=-999999
max[4]=-999999
max[5]=-999999
max[6]=-999999

## grab data to find the max and min for each of the 6 graphs
while read temp
  do
  num[1]=`echo $temp | awk -F[" ".] '{print $1$2}' `
  num[2]=`echo $temp | awk -F[" ".] '{print $3$4}' `
  num[3]=`echo $temp | awk -F[" ".] '{print $5$6}' `
  num[4]=`echo $temp | awk -F[" ".] '{print $7$8}' `
  num[5]=`echo $temp | awk -F[" ".] '{print $9$10}' `
  num[6]=`echo $temp | awk -F[" ".] '{print $11$12}' `
  echo ${num[1]} ${num[2]} ${num[3]} ${num[4]} ${num[5]} ${num[6]}
  num_of_runs=0
  while [ $num_of_runs -lt 6 ]
    do
    num_of_runs=`expr $num_of_runs + 1`
    if [ ${num[$num_of_runs]} -lt ${min[$num_of_runs]} ]; then
	min[$num_of_runs]=${num[$num_of_runs]}
    fi   
    if [ ${num[$num_of_runs]} -gt ${max[$num_of_runs]} ]; then
	max[$num_of_runs]=${num[$num_of_runs]}
    fi
  done
done < testing.1D
echo finding minimum and maximum roll, pitch, yaw, dS, dL, dP
echo minimums: ${min[1]} ${min[2]} ${min[3]} ${min[4]} ${min[5]} ${min[6]}
echo maximums: ${max[1]} ${max[2]} ${max[3]} ${max[4]} ${max[5]} ${max[6]}

## calculate the average value of the max and min, this finds the center line
echo calculate average value of minimum and maximum motion parameters to find best fit line 
num_of_runs=0
while [ $num_of_runs -lt 6 ]
  do
  num_of_runs=`expr $num_of_runs + 1`
  av[$num_of_runs]=`expr ${min[$num_of_runs]} + ${max[$num_of_runs]}`
  av[$num_of_runs]=`expr ${av[$num_of_runs]} / 2`
done
echo average is: ${av[1]}, ${av[2]}, ${av[3]}, ${av[4]}, ${av[5]}, ${av[6]}

min=999999
counter=0

#check all values to find a set which is closes to the average over all
echo check all values to find a set which is closes to the average over all

min=999999
counter=0
while read temp
  do
  counter=`expr $counter + 1`
  con=1
  num[1]=`echo $temp | awk -F[" ".] '{print $1$2}' `
  num[2]=`echo $temp | awk -F[" ".] '{print $3$4}' `
  num[3]=`echo $temp | awk -F[" ".] '{print $5$6}' `
  num[4]=`echo $temp | awk -F[" ".] '{print $7$8}' `
  num[5]=`echo $temp | awk -F[" ".] '{print $9$10}' `
  num[6]=`echo $temp | awk -F[" ".] '{print $11$12}' `
  echo Checking ${num[1]} ${num[2]} ${num[3]} ${num[4]} ${num[5]} ${num[6]}

  #each TR, calculate distance of each motion parameter from from average motion parameter.
  num_of_runs=0
  while [ $num_of_runs -lt 6 ]
    do    
    num_of_runs=`expr $num_of_runs + 1`
    dif[$num_of_runs]=`expr ${av[$num_of_runs]} - ${num[$num_of_runs]}`
    if [ ${dif[$num_of_runs]} -lt 0 ]; then
	dif[$num_of_runs]=`expr ${dif[$num_of_runs]} \* -1`
    fi
  done
  num_of_runs=0
  compare=-10
  while [ $num_of_runs -lt 6 ]
    do    
    num_of_runs=`expr $num_of_runs + 1`
    if [ ${dif[$num_of_runs]} -gt $compare ]; then
	compare=${dif[$num_of_runs]}
    fi
  done
  if [ $min -ge $compare ] && [ `expr $counter % $volume` -gt 10 ]; then
      echo $min, $compare, $counter
      min=$compare
      final=$counter
  fi
done < testing.1D

#The subbrik number is calculated 
echo $final
echo $min

run_number=`expr $final / $volume + 1`
brik_number=`expr $final % $volume`

echo The minimum distance found was $min from average
echo motion correction will be based on run$run_number subbrik $brik_number

## realign based on the computer calculated value, for graphical display
3dvolreg -prefix temp1 -base "run$run_number+orig[$brik_number]" -zpad 2 -twopass -twodup -Fourier -1Dfile temp.1D -dfile temp1dfile all_PTruns+orig   
1dplot -volreg temp.1D &

##Realigning individual runs using the values choosen above
num_of_runs=0
while [ $num_of_runs -lt $num_runs ]
  do
  num_of_runs=`expr $num_of_runs + 1`
  echo "Motion correction for run"$num_of_runs" based on above info"
  3dvolreg -prefix PTRrun$num_of_runs -base "run$run_number+orig[$brik_number]" -zpad 2 -1Dfile run$num_of_runs.1D -twopass -twodup -Fourier PTrun$num_of_runs+orig
  1dplot -volreg run$num_of_runs.1D &
done
fi

###############

########################################################
if [ $talaraich = "y" ]; 
then 
#talaraich anatomical

num_of_parts=0
while [ $num_of_parts -lt $num_parts ]
  do 
  num_of_parts=`expr $num_of_parts + 1`
  
echo running transformation for $home$num_of_parts
  cd $home/${tbir[$num_of_parts]}/afdir
  echo transform anatomical dataset to match TT_avg152 brain
  @auto_tlrc -base TT_avg152T1+tlrc -input "$anat_name"+orig -suffix _ref_avg152T1 -ok_notice -OK_maxite
  rm 3dvol_ns*
  echo transform 3dvol+orig by same TLRC transformation obtained 'in' first step
  @auto_tlrc -apar "$anat_name"_ref_avg152T1+tlrc -input "$anat_name"+orig -suffix _avg152 -OK_maxite
 ##talaraich functional data
  num_of_runs=0
  while [ $num_of_runs -lt $num_runs ]
    do 
    num_of_runs=`expr $num_of_runs + 1`
    echo transforming motion corrected functional data using same transformation as above
    @auto_tlrc -apar 3dvol_ref_avg152T1+tlrc -input PTRrun$num_of_runs+orig -suffix _avg152T1 -OK_maxite -dx 4 -dy 4 -dz 4
  done 

#### spatial smoothing

num_of_runs=0

while [ $num_of_runs -lt $num_runs ]
do

num_of_runs=`expr $num_of_runs + 1`
echo smoothing for ${tbir[$num_of_parts]} run$num_of_runs
3dmerge -doall -prefix sPTRrun"$num_of_runs"_"avg152T1+tlrc" -1blur_fwhm 8 PTRrun"$num_of_runs"_avg152T1+tlrc

done

##convert to nii 

  num_of_runs=0
  while [ $num_of_runs -lt $num_runs ]
    do
    num_of_runs=`expr $num_of_runs + 1`
    echo converting functional data for run$num_of_runs to NIFTI
    3dAFNItoNIFTI sPTRrun"$num_of_runs"_avg152T1+tlrc
  done

echo cleaning up...

mkdir for_PLS
  mv PTRrun*_avg* for_PLS
 mv sPTRrun*_avg* for_PLS 
cd for_PLS
  chmod 777 *

  echo done $home/${tbir[$num_of_parts]}
  cd $home  
done
fi
#############

if [ $collate = "y" ];then
num_of_parts=0
while [ $num_of_parts -lt $num_parts ]
  do 
  num_of_parts=`expr $num_of_parts + 1`
  
echo moving files for $home/$num_of_parts
  cd $home/${tbir[$num_of_parts]}/afdir/for_PLS

mv sPTRrun1_avg152T1.nii $home/for_PLS/${tbir[$num_of_parts]}_sPTRrun1_avg152T1.nii
mv sPTRrun2_avg152T1.nii $home/for_PLS/${tbir[$num_of_parts]}_sPTRrun2_avg152T1.nii
mv sPTRrun3_avg152T1.nii $home/for_PLS/${tbir[$num_of_parts]}_sPTRrun3_avg152T1.nii
done
fi
