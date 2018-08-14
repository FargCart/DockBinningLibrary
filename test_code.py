import pymol
from pymol import cmd
from pymol import stored
import os
#import FileWriter as fw
import csv
import time
import datetime

# launch pymol without gui
pymol.finish_launching(['pymol', '-c'])


cmd.do("run renumber.py")
clistAB1=['H','L']
clistAB2=['M','N']

#Making empty lists
stored.residues1=[]
stored.residues2=[]
stored.resN1=[]
stored.resN2=[]

#setting ab variables
mAb1="1D3__Ligand_1_000_00.pdb"
mAb2="Ab2.pdb"


final=[]

#loading and changing appropriate chains
cmd.load(mAb1)
cmd.do('alter (chain H), chain="M"')
cmd.do('alter (chain L), chain="N"')
cmd.load(mAb2)

#quality assurance of numbering of residues
cmd.do("renumber chain H,1")
cmd.do("renumber chain L,1")
cmd.do("renumber chain M,1")
cmd.do("renumber chain N,1")


#making the titles
titlelist=['1_Residue #','1_Residue Name','2_Residue #','2_Residue Name','Calpha','Centroid','MinDistance']

#for the loop counter
r=0

overalltime = time.time();
#totalres= int(len(stored.residues1))*int(len(stored.residues2))
with open("test_output.csv", 'wb') as resultFile:
    wr=csv.writer(resultFile,delimiter=",",dialect="excel")
    Medium = 0;
    for ab1 in range(0,2):
        cmd.iterate("(chain "+str(clistAB1[ab1])+" and n. CA)", "stored.residues1.append((resi))")
        cmd.iterate("(chain "+str(clistAB1[ab1])+" and n. CA)", "stored.resN1.append((resn))")
        for ab2 in range(0,2):
            cmd.iterate("(chain "+str(clistAB2[ab2])+" and n. CA)", "stored.residues2.append((resi))")
            cmd.iterate("(chain "+str(clistAB2[ab2])+" and n. CA)", "stored.resN2.append((resn))")
            for i in range(0,len(stored.residues1)):
                for b in range(0,len(stored.residues2)):
                    starttime = time.time();
                    myresname1=(stored.resN1[i])
                    myresnumber1=(stored.residues1[i])
                    myresname2=(stored.resN2[b])
                    myresnumber2=(stored.residues2[b])

                    #Heavy chain interactions
                    Calpha =str(round(cmd.distance('output', 'chain '+str(clistAB1[ab1])+' and i. ' + str(i+1) + ' and n. CA', 'chain '+str(clistAB2[ab2])+' and i. ' + str(b+1) + ' and n. CA'),1))

                    # #Light chain interactions
                    # CalphaL1 = str(round(cmd.distance('output', 'chain L and i. ' + str(i + 1) + ' and n. CA','chain M and i. ' + str(b + 1) + ' and n. CA'), 1))
                    # CalphaL2 = str(round(cmd.distance('output', 'chain L and i. ' + str(i + 1) + ' and n. CA','chain N and i. ' + str(b + 1) + ' and n. CA'), 1))

                    # Centroid = str(round(cmd.distance('output', 'chain H and i. ' + str(i + 1), 'chain L and i. ' + str(b + 1),-1, 4), 1))
                    # if x < = Minimum || Medium = 0:
                    #     Medium = x
                    r=r+1
                    # if (r % 500) <= 0:
                    print("running "+str(r)+"/"+str(int(len(stored.residues1))*int(len(stored.residues2)))) + ' : Remaining Time:',
                    averagetime = time.time() - (overalltime/r)
                    remaintime = (time.time() - overalltime)/r * ((int(len(stored.residues1))*int(len(stored.residues2))) - r)
                    print datetime.timedelta(seconds=remaintime)


                   # if remaintime > datetime.timedelta(seconds=0):
        #                print(str(remaintime))
        #            else:

        #                print('Job complete!')

                    final.append('\n')
                    final.append(str(clistAB1[ab1]))
                    final.append(myresname1)
                    final.append(myresnumber1)
                    final.append(str(clistAB2[ab2]))
                    final.append(myresname2)
                    final.append(myresnumber2)
                    final.append(Calpha)
                    # final.append(Centroid)

            wr.writerows([final])




# print(stored.residues1)
# print(len(stored.residues1))
# print(stored.residues2)
# print(len(stored.residues2))

f.write(str(final))
f.close
