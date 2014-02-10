%batch creation of oba.slibase filesv
% j = subject number
% day1, day2 binary flags (0 or 1)
function RVTbatch(j, day1, day2)
cd /misc/data69/stevenswd/COP/DATA/FMRI/


    
    subj_folder = dir(['1*3TB*0' num2str(j)]);
    cd(subj_folder.name)
    
    if day1==1
    cd A/RT/
    delete oba.slibase*
    delete *RVT*
    ECGs = dir('ecg.*.loc*');
    RESPs = dir('resp.*.loc*');
    
    run = ECGs(1).name;
    subjnum  = run(6:7);

    for i = 1:length(ECGs)
        
        A = textread(ECGs(i).name);
        B = textread(RESPs(i).name);
        if (length(A) == 21900) && (length(B) == 21900)
            
            run = ECGs(i).name;
            runnum = run(12:13);
            
            Opt.Respfile = RESPs(i).name;
            Opt.Cardfile = ECGs(i).name;
            Opt.VolTR = 2.0;
            Opt.Nslices = 41;
            Opt.PhysFS = 1./0.02;
            RetroTS(Opt);
            
            movefile('oba.slibase.1D', strcat('oba.slibase.s',subjnum,'.',runnum,'.1D'));
        else
            strcat('WARNING:: There is an issue with phsyio data for run ', runnum)
        end
    end
    
    if j == 10
        ECGrest = dir('ecg.*.rest01.1D');
        RESPrest = dir('resp.*.rest01.1D');
    else
        ECGrest = dir('ecg.*.rest*');
        RESPrest = dir('resp.*.rest*');
    end
    
    for i = 1:length(ECGrest)
        A = textread(ECGrest(i).name);
        B = textread(RESPrest(i).name);
        if (length(A) == 24500) && (length(B) == 24500)
            Opt.Respfile = RESPrest(i).name;
            Opt.Cardfile = ECGrest(i).name;
            Opt.VolTR = 3.5;
            Opt.Nslices = 42;
            Opt.PhysFS = 1./0.02;
            RetroTS(Opt);
            movefile('oba.slibase.1D', strcat('oba.slibase.s',subjnum,'.rest0',num2str(i),'.1D'));
        else
            strcat('WARNING:: There is an issue with phsyio data for REST run ', runnum)
        end
    end
    
    cd ../../..
    
end
if day2==1
    
    subj_folder = dir(['1*3TB*0' num2str(j)]);
    cd(subj_folder.name)
    cd B/RT/
    delete oba.slibase*
    delete *RVT*
    ECGs = dir('ecg.*.task*');
    RESPs = dir('resp.*.task*');
    
    run = ECGs(1).name;
    subjnum  = run(6:7);
    
    for i = 1:length(ECGs)
        
        A = textread(ECGs(i).name);
        B = textread(RESPs(i).name);
        if (length(A) == 22200) && (length(B) == 22200)
            
            run = ECGs(i).name;
            runnum = run(13:14);
            
            Opt.Respfile = RESPs(i).name;
            Opt.Cardfile = ECGs(i).name;
            Opt.VolTR = 2.0;
            Opt.Nslices = 41;
            Opt.PhysFS = 1./0.02;
            RetroTS(Opt);
            
            movefile('oba.slibase.1D', strcat('oba.slibase.s',subjnum,'.task',runnum,'.1D'));
        else
            strcat('WARNING:: There is an issue with phsyio data for run ', runnum)
        end
    end
    cd ../../../
end
   cd ../scripts/GENPROC/
   end



%AFNI 1dcat oba.slibase.s16.loc01.1D'[0..4]{4..218}' > s16.loc01.RVT.1D
