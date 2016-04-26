% 6pt5.nii & 8pt5.nii = the 4 volume sets with magnitude, phase, real, imaginary for each TE 
% refset.nii = the 2 volume set with reference PDW and T2W scans 
% dti.nii = the multivolume dti data set 

fslsplit ~/6pt5 ~/6pt5 -t 
fslsplit ~/8pt5 ~/8pt5 -t 
bet ~/6pt50000 ~/6pt5magbet -m 
bet ~/8pt50000 ~/8pt5magbet -m 

# deskull real/imag for both TEs
fslmaths ~/6pt50002 -mul ~/6pt5magbet_mask ~/6pt5real -odt float 
fslmaths ~/8pt50002 -mul ~/8pt5magbet_mask ~/8pt5realbet -odt float 
fslmaths ~/6pt50003 -mul ~/6pt5magbet_mask ~/6pt5imag -odt float 
fslmaths ~/8pt50003 -mul ~/8pt5magbet_mask ~/8pt5imagbet -odt float 
flirt -in ~/8pt5magbet -ref ~/6pt5magbet -out ~/8pt5um -omat ~/8pt5matrix 
flirt -in ~/8pt5realbet -ref ~/6pt5magbet -applyxfm -init ~/8pt5matrix -out ~/8pt5real 
flirt -in ~/8pt5imagbet -ref ~/6pt5magbet -applyxfm -init ~/8pt5matrix -out ~/8pt5imag 

TE6pt5real=load_nii('~/6pt5real.nii'); TE6pt5real=TE6pt5real.img; 
TE6pt5imag=load_nii('~/6pt5imag.nii'); TE6pt5imag=TE6pt5imag.img; 
TE8pt5real=load_nii('~/8pt5real.nii'); TE8pt5real=TE8pt5real.img; 
TE8pt5imag=load_nii('~/8pt5imag.nii'); TE8pt5imag=TE8pt5imag.img; 
TE6pt5complex = complex(TE6pt5real,TE6pt5imag); 
TE8pt5complex = complex(TE8pt5real,TE8pt5imag); 

mul = conj(TE6pt5complex).*TE8pt5complex; 
abs=abs(mul); 
abs=make_nii(abs,[220/64 220/64 4]); save_nii(abs,'~/abs.nii'); 
phase = angle(mul); 
phase=make_nii(phase,[220/64 220/64 4]); save_nii(phase,'~/phase.nii'); 

prelude -p ~/phase -a ~/abs -o ~/phaseunwrapped 

phase=load_nii('~/phaseunwrapped.nii'); phase=phase.img; 
map = phase./0.002; 
fieldmap=make_nii(map,[220/64 220/64 4]); save_nii(fieldmap, '~/fieldmap.nii'); 

flirt -in ~/abs -ref ~/T2bet -omat ~/TEtoT2 
flirt -in ~/fieldmap -ref ~/T2bet -applyxfm -init ~/TEtoT2 -out ~/fmap 
fugue -i ~/dtieddybet --loadfmap=/home/jchad/fmap --dwell=0.000684 -u ~/dtifinal –poly=3 
dtifit -k ~/dtifinal -m ~/PDWbet_mask -r ~/vec.bvec -b ~/val.bval -o ~/dtifit