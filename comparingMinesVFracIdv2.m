opts = spreadsheetImportOptions("NumVariables", 41);
opts.Sheet = "allStep_wRadialVel";
opts.DataRange = "A3:AO10196";
opts.VariableNames = ["step", "time", "Q1w", "Q1x", "Q1y", "Q1z", "Px", "Py", "Pz", "S", "S_DOT", "S_DDOT", "BORE_Uy", "BORE_Uz", "Q2w", "Q2x", "Q2y", "Q2z", "w12x", "w12y", "w12z", "w12x_dot", "w12y_dot", "w12z_dot", "Oy", "Oz", "OVel_y", "OVel_z", "OAccel_y", "OAccel_z", "THETA", "drill_speed", "drill_speed_dot", "G_MAG", "AngX", "AngY", "AngZ", "Ax", "Ay", "Az", "radialVel"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

opts2 = spreadsheetImportOptions("NumVariables",4);
opts2.Sheet = "synthetic-11Update";
opts2.DataRange = "A2:D10200";
opts2.VariableTypes = ["double", "double", "double", "double"];
MinesData = readtable("C:\Users\chris\Documents\research\comparing MinesVSynthetic11data_nographs.xlsx", opts, "UseExcel", false);
FracID_Data = readtable("C:\Users\chris\Documents\research\comparing MinesVSynthetic11data_nographs.xlsx", opts2, "UseExcel", false);

fracIDAccel = table2array(FracID_Data(2:10195,2:4));
minesAccel = table2array(MinesData(:,38:40));
t = table2array(MinesData(:,2));

y1 = fracIDAccel;
y2 = minesAccel;
% error
dy = y2-y1 ;
labels = ["Mines X","Mines Y", "Mines Z";"FracID X", "FracID Y", "FracID Z";"Error X","Error Y","Error Z"];

for i=1:3
    figure
    hold on
    subplot(3,1,1);
    plot(t,y2(:,i),'k');
    legend(labels(1,i))

    subplot(3,1,2);
    plot(t,y1(:,i),'b')
    legend(labels(2,i))

    subplot(3,1,3);
    plot(t,dy(:,i),'r');
    legend(labels(3,i))
end