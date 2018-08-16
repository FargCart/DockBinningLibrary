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
calphaCutoff = str(round(10))

#Making empty lists
stored.residues1 = []
stored.residues2 = []
stored.resN1 = []
stored.resN2 = []
minimumList=[]
stored.t2 = []
stored.t3 = []

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

# Opening CSV file for writting.
with open(destfile, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(titleList)

    Medium = 0;
    # Loop for first two chains.
    for aB1 in range(0,2):
        stored.residues1 = []
        stored.resN1 = []
        cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                    "stored.residues1.append((resi))")
        cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                    "stored.resN1.append((resn))")
        # Loop for second two chains.
        for aB2 in range(0,2):
            stored.residues2 = []
            stored.resN2 = []
            cmd.iterate("(chain "+str(clistAb2[aB2])+" and n. CA)",
                        "stored.residues2.append((resi))")
            cmd.iterate("(chain "+str(clistAb2[aB2])+" and n. CA)",
                        "stored.resN2.append((resn))")
            # Loop for running through all residues for 1st mAb.
            for firstAb in range(0, len(stored.residues1)):
                # Loop for running through all residues for 2nd mAb.
                for secondAb in range(0, len(stored.residues2)):
                    final = []
                    # stored.t2=[]
                    # stored.t3=[]

                    cmd.iterate('(chain '+str(clistAb1[aB1])+' and i. '+str(firstAb)+')'
                                , 'stored.t2.append((name))')
                    cmd.iterate('(chain '+str(clistAb1[aB2])+' and i. '+str(secondAb)+')'
                                , 'stored.t3.append((name))')

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
                    if (totalRuns % 5000) <= 0:
                        print("Good Values  " + str(goodRuns)
                              + '\n'
                              + "Total Runs " + str(totalRuns))

                    if float(0) < float(cAlpha) < float(calphaCutoff):

                        centRoid = str(round(cmd.distance('output', 'chain ' + str(
                            clistAb1[aB1]) + ' and i. '
                                                          + str(firstAb + 1),
                                                          'chain ' + str(
                                                              clistAb2[aB2]) + ' and i. '
                                                          + str(secondAb + 1), -1, 4),1))
                        goodRuns = goodRuns + 1

                        # for atomTest in range(1,len(stored.t2)):
                        #     for atomTest2 in range(1,len(stored.t3)):
                        #         # minimumList=[]
                        #         minCalc = str(round(cmd.distance('output2', 'chain '+str(clistAb1[aB1])
                        #                                          + ' and i. '+str(firstAb)+' and n. '
                        #                                          + str(stored.t2[atomTest]), 'chain '
                        #                                          + str(clistAb2[aB2])
                        #                                          + ' and i. '+str(secondAb)
                        #                                          + ' and n. '
                        #                                          + str(stored.t3[atomTest2])), 1))
                        #         minimumList.append(minCalc)
                        #         minMum = min(minimumList)
                        #         print(minMum)

                        # if (r % 5000) < = 0:
                        # print("running "+str(r)+"/"+str(int(len(stored.residues1))*int(len(stored.residues2)))) \
                        #      + ' : Remaining Time:',

                        # averageTime = time.time() - (overallTime/totalRuns)
                        # remainTime = (time.time() - overallTime)/totalRuns \
                        #              * ((int(len(stored.residues1))
                        #             * int(len(stored.residues2))) - totalRuns)
                        # print datetime.timedelta(seconds=remainTime)

                        final.extend([str(clistAb1[aB1]), myresNumber1,
                                      myresName1, placeHolder, str(clistAb2[aB2]),
                                      myresNumber2, myresName2,
                                      cAlpha, centRoid])
                        csvwriter.writerow(final)
                    else:
                        pass
                    

t1 = time.time()
tTime = t1-t0
#print("Total Time = "+str(tTime))
#print(totalRuns)
                   # if remainTime > datetime.timedelta(seconds = 0):
        #                print(str(remainTime))
        #            else:

        #                print('Job complete!')


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