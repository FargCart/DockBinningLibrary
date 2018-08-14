import os

import csv

import time

import datetime

import pymol

from pymol import cmd

from pymol import stored


''' Will be using mixedCaps style '''

# launch pymol without gui
pymol.finish_launching(['pymol', '-c'])

t0 = time.time()
destfile = "output.csv"
cmd.do("run renumber.py")
clistAb1 = ['H', 'L']
clistAb2 = ['M', 'N']
calphaCutoff = str(float(10))

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
titleList = ['Chain', '1_Residue #', '1_Residue Name',' ', 'Chain', '2_Residue #', '2_Residue Name', 'cAlpha','centRoid', 'MinDistance']

#for the loop counter
totalRuns = 0
goodRuns = 0


overallTime = time.time();
#totalres = int(len(stored.residues1))*int(len(stored.residues2))
with open(destfile, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(titleList)
    Medium = 0;
    for aB1 in range(0,2):
        stored.residues1 = []
        stored.resN1 = []
        cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                    "stored.residues1.append((resi))")
        cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                    "stored.resN1.append((resn))")
        for aB2 in range(0,2):
            stored.residues2 = []
            stored.resN2 = []
            cmd.iterate("(chain "+str(clistAb2[aB2])+" and n. CA)",
                        "stored.residues2.append((resi))")
            cmd.iterate("(chain "+str(clistAb2[aB2])+" and n. CA)",
                        "stored.resN2.append((resn))")
            for firstAb in range(0, len(stored.residues1)):
                for secondAb in range(0, len(stored.residues2)):
                    final = []
                    stored.t2=[]
                    stored.t3=[]
                    ##this is where i am working on for the min
                    cmd.iterate('(chain '+str(clistAb1[aB1]+' and i. '+str(firstAb),
                                'stored.t2.append((name))'))
                    cmd.iterate('(chain '+str(clistAb1[aB2]+' and i. '+str(secondAb),
                                'stored.t2.append((name))'))
                    starttime = time.time();
                    myresName1 = (stored.resN1[firstAb])
                    myresNumber1 = (stored.residues1[firstAb])
                    myresName2 = (stored.resN2[secondAb])
                    myresNumber2 = (stored.residues2[secondAb])
                    placeHolder=' '

                    #cAlpha Calculation
                    cAlpha = str(round(cmd.distance('output', 'chain '
                                                    + str(clistAb1[aB1])
                                                    + ' and i. ' + str(firstAb+1)
                                                    + ' and n. CA', 'chain '
                                                    +str(clistAb2[aB2])+' and i. '
                                                    + str(secondAb+1)
                                                    + ' and n. CA'),1))
                    totalRuns = totalRuns+1

                    if cAlpha > calphaCutoff:
                        pass
                    else:

                    #centRoid Calculation
                        centRoid = str(round(cmd.distance('output', 'chain H and i. '
                                                          + str(firstAb + 1), 'chain L and i. '
                                                          + str(secondAb + 1),-1, 4), 1))

                    # for atom1 in range(secondAb):
                    #     for atom2 in range(firstAb):
                    #         distance = sqrt((atom1.elem.x - atom2.elem.x)^2 +
                    #                         (atom1.elem.y - atom2.elem.y)^2 +
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
                        print("Good Values  "+ str(goodRuns)
                              + '\n'
                              + "Total Runs "+ str(totalRuns))
                        averageTime = time.time() - (overallTime/totalRuns)
                        remainTime = (time.time() - overallTime)/totalRuns \
                                     * ((int(len(stored.residues1))
                                    * int(len(stored.residues2))) - totalRuns)
                        # print datetime.timedelta(seconds=remainTime)

                        final.extend([str(clistAb1[aB1]), myresName1,
                                      myresNumber1, placeHolder, str(clistAb2[aB2]),
                                      myresName2, myresNumber2,
                                      cAlpha, centRoid])
                        csvwriter.writerow(final)
                    

t1 = time.time()
tTime = t1-t0
print("Total Time = "+str(tTime))
print(totalRuns)
                   # if remainTime > datetime.timedelta(seconds = 0):
        #                print(str(remainTime))
        #            else:

        #                print('Job complete!')







