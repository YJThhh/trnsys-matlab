


Te_in=12;
Ge_in=8;
Tc_in=35;
Gc_in=3;


options = simset('SrcWorkspace','current','Solver','ode15s','MaxStep','0.2');

out = sim('autoArrange',[0,3], options);




getdatasamples(out.simout1, [get(out.simout1).Length])