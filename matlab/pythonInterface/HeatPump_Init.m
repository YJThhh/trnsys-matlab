function outputArg = HeatPump_Init(inputArg)
    disp('call HeatPump_Init')

    persistent tcw12
    persistent tc
    persistent h3
    persistent tew12
    persistent te
    persistent h1

    persistent Te_in
    persistent Ge_in
    persistent Tc_in
    persistent Gc_in


    tcw12 = 70;
    tc = 50;
    h3 = 260;
    tew12 = 20;
    te = 5;
    h1 =  410;  

    Te_in=12;
    Ge_in=14;
    Tc_in=35;
    Gc_in=8;


    options = simset('SrcWorkspace','current','Solver','ode45');
    out = sim('H_P.slx',[0, 0.01], options);


    outputArg(1) = getdatasamples(out.pc, [get(out.tcw12).Length]);
    outputArg(2) = getdatasamples(out.tcw2, [get(out.tcw12).Length]);
    outputArg(3) = getdatasamples(out.h3, [get(out.tcw12).Length]);
    outputArg(4) = getdatasamples(out.Qc, [get(out.tcw12).Length]);
    outputArg(5) = getdatasamples(out.tew2, [get(out.tcw12).Length]);
    outputArg(6) = getdatasamples(out.pe, [get(out.tcw12).Length]);
    outputArg(7) = getdatasamples(out.h1, [get(out.tcw12).Length]);
    outputArg(8) = getdatasamples(out.vd, [get(out.tcw12).Length]);
    outputArg(9) = getdatasamples(out.Qe, [get(out.tcw12).Length]);
end

