import pymol
from pymol import cmd
from pymol import stored
import os
import csv
import time
import datetime

# launch pymol without gui
pymol.finish_launching(['pymol', '-c'])

t0 = time.time()
destfile = "output.csv"
cmd.do("run renumber.py")
clistAB1 = ['H', 'L']
clistAB2 = ['M', 'N']
calphacutoff = str(float(10))

#Making empty lists
stored.residues1 = []
stored.residues2 = []
stored.resN1 = []
stored.resN2 = []

#setting ab variables
mAb1 = "1D3__Ligand_1_000_00.pdb"
mAb2 = "Ab2.pdb"


final = []

#loading and changing appropriate chains
cmd.load(mAb1)
cmd.do('alter (chain H), chain = "M"')
cmd.do('alter (chain L), chain = "N"')
cmd.load(mAb2)

#quality assurance of numbering of residues
cmd.do("renumber chain H,1")
cmd.do("renumber chain L,1")
cmd.do("renumber chain M,1")
cmd.do("renumber chain N,1")


#making the titles
titlelist = ['1_Residue #', '1_Residue Name', '2_Residue #', '2_Residue Name', 'Calpha','Centroid', 'MinDistance']

#for the loop counter
totalRuns = 0
goodRuns = 0


overalltime = time.time();
#totalres = int(len(stored.residues1))*int(len(stored.residues2))
with open(destfile, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(titlelist)
    Medium = 0;
    for ab1 in range(0,2):
        cmd.iterate("(chain "+str(clistAB1[ab1])+" and n. CA)", "stored.residues1.append((resi))")
        cmd.iterate("(chain "+str(clistAB1[ab1])+" and n. CA)", "stored.resN1.append((resn))")
        for ab2 in range(0,2):
            cmd.iterate("(chain "+str(clistAB2[ab2])+" and n. CA)", "stored.residues2.append((resi))")
            cmd.iterate("(chain "+str(clistAB2[ab2])+" and n. CA)", "stored.resN2.append((resn))")
            for i in range(0, len(stored.residues1)):
                for b in range(0, len(stored.residues2)):
                    final = []
                    starttime = time.time();
                    myresname1 = (stored.resN1[i])
                    myresnumber1 = (stored.residues1[i])
                    myresname2 = (stored.resN2[b])
                    myresnumber2 = (stored.residues2[b])

                    #Calpha Calculation
                    Calpha = str(round(cmd.distance('output', 'chain '+str(clistAB1[ab1])+' and i. ' + str(i+1) +
                                                    ' and n. CA', 'chain '+str(clistAB2[ab2])+' and i. ' + str(b+1)
                                                    + ' and n. CA'),1))
                    totalRuns = totalRuns+1
                    if Calpha > calphacutoff:
                        pass
                    else:

                    #Centroid Calculation
                        Centroid = str(round(cmd.distance('output', 'chain H and i. ' + str(i + 1), 'chain L and i. '
                                                          + str(b + 1),-1, 4), 1))

                    # for atom1 in range(b):
                    #     for atom2 in range(i):
                    #         distance = sqrt((atom1.elem.x - atom2.elem.x)^2 + (atom1.elem.y - atom2.elem.y)^2 +
                    #                         (atom1.elem.z - atom2.elem.z)^2)
                    #         print(str(atom1.elem + ' ' + atom2.elem + ' '),
                    #         print(str(distance))
                    #         if distance < = Minimum || Medium = 0:
                    #              Medium = distance
                    #
                    # Minimum = str(Medium)

                        goodRuns = goodRuns+1
                        # if (r % 5000) < = 0:
                        # print("running "+str(r)+"/"+str(int(len(stored.residues1))*int(len(stored.residues2)))) \
                        #      + ' : Remaining Time:',
                        print("Good Values  " + str(goodRuns) + '\n' + "Total Runs " + str(totalRuns))
                        averagetime = time.time() - (overalltime/totalRuns)
                        remaintime = (time.time() - overalltime)/totalRuns * ((int(len(stored.residues1))
                                                                               *int(len(stored.residues2))) - totalRuns)
                        print datetime.timedelta(seconds=remaintime)

                        final.extend([str(clistAB1[ab1]), myresname1, myresnumber1, str(clistAB2[ab2]),
                                      myresname2, myresnumber2, Calpha, Centroid])
                        csvwriter.writerow(final)
                    

t1 = time.time()
Ttime = t1-t0
print("Total Time = "+str(Ttime))
                   # if remaintime > datetime.timedelta(seconds = 0):
        #                print(str(remaintime))
        #            else:

        #                print('Job complete!')







