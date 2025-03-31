load BandStructure.mat;
data
kindex = 1:data.numberOfKPoints;
HATREE2EV = 27.211383438808717;
if(numel(data.bandEnergies) == 1)
    writematrix([kindex', data.bandEnergies{1}'*HATREE2EV], 'bandEnergies.dat');
else
    writematrix([kindex', data.bandEnergies{1}'*HATREE2EV], 'bandEnergies_up.dat');
    writematrix([kindex', data.bandEnergies{2}'*HATREE2EV], 'bandEnergies_dn.dat');
end
