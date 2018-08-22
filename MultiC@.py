import os

import csv

import time

import datetime

import pymol

from pymol import cmd

from pymol import stored

from pymol import math

import sys

import renumber





''' Will be using mixedCaps style '''



os.system('rm -rf pdbFiles')
# launch pymol without gui
pymol.finish_launching(['pymol', '-c'])

t0 = time.time()
destfile = "output.csv"
cmd.do("run renumber.py")
# clistAb1 = ['H', 'L']
# clistAb2 = ['M', 'N']
calphaCutoff = str(round(5))

os.system("mkdir pdbFiles")
cmd.load("3_ab_test.mae")
fullList=cmd.get_object_list('all')

#Making empty lists
stored.residues1 = []
stored.residues2 = []
stored.resN1 = []
stored.resN2 = []
minimumList=[]
stored.t2 = []
stored.t3 = []
totalTime = 0


# print("Making PDB files...")
for x in range(0, len(fullList)):
    ab = []
    ab = fullList[x].split('.')[1]
    cmd.save(os.getcwd()+'/pdbFiles/'+ab+'.pdb',fullList[x])
    
# print("PDB files generated!")


cmd.reinitialize()
os.chdir("pdbFiles")
dirlist=os.listdir(".")
dirlist=sorted(dirlist)
os.chdir("..")
secondStart = 0

#making the titles
titleList = ['Antibody 1', ' ', 'Antibody 2', 'cAlpha', 'centRoid', 'MinDistance']
abT1 = time.time()
with open(destfile, 'wb') as csvfile:
    os.chdir("pdbFiles")
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(titleList)
    for loadfirst in range(0,len(dirlist)):


        cmd.load(dirlist[loadfirst])
        abTemp=(cmd.get_object_list('all'))
        noExt1 = dirlist[loadfirst].split('.')
        cmd.alter(str(noExt1[0])+' and chain H', 'chain = "'+str(noExt1[0])+'.H"')
        cmd.alter(str(noExt1[0])+' and chain L', 'chain = "'+str(noExt1[0])+'.L"')
        renumber.renumber('chain ' + str(noExt1[0]) + '.H', 1)
        renumber.renumber('chain ' + str(noExt1[0]) + '.L', 1)

        clistAb1 = cmd.get_chains()
        # print(clistAb1)
        secondStart = secondStart + 1


        for loadsecond in range(secondStart,len(dirlist)):

            cmd.load(dirlist[loadsecond])
            noExt2 = dirlist[loadsecond].split('.')
            cmd.alter(str(noExt2[0])+' and chain H', 'chain = "' + str(noExt2[0]) + '.H"')
            cmd.alter(str(noExt2[0])+' and chain L', 'chain = "' + str(noExt2[0]) + '.L"')
            renumber.renumber('chain ' + str(noExt2[0]) + '.H', 1)
            renumber.renumber('chain ' + str(noExt2[0]) + '.L', 1)
            clistAb2 = cmd.get_chains(str(noExt2[0]))
            # print(clistAb2)
            final = []
            #for the loop counter
            totalRuns = 0
            # goodRuns = 0
            overallTime = time.time();
            # Opening CSV file for writing.
            Medium = 0;
            # Loop for first two chains.
            for aB1 in range(0, 2):

                stored.residues1 = []
                stored.resN1 = []
                cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                            "stored.residues1.append((resi))")
                cmd.iterate("(chain "+str(clistAb1[aB1])+" and n. CA)",
                            "stored.resN1.append((resn))")
                # Loop for second two chains.
                for aB2 in range(0, 2):


                    tS = time.time()

                    print(str(clistAb1[aB1])+' : '+str(clistAb2[aB2]))
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
        
        
                            cmd.iterate('(chain '+str(clistAb1[aB1])+' and i. '+str(firstAb)+')'
                                        , 'stored.t2.append((name))')
                            cmd.iterate('(chain '+str(clistAb1[aB2])+' and i. '+str(secondAb)+')'
                                        , 'stored.t3.append((name))')
        
                            starttime = time.time();
                            myresName1 = (stored.resN1[firstAb])
                            myresNumber1 = (stored.residues1[firstAb])
                            myresName2 = (stored.resN2[secondAb])
                            myresNumber2 = (stored.residues2[secondAb])
                            placeHolder = ' '
        
        
                            #cAlpha Calculation
                            cAlpha = str(round(cmd.distance('output', 'chain '
                                                            + str(clistAb1[aB1])
                                                            + ' and i. ' + str(firstAb+1)
                                                            + ' and n. CA', 'chain '
                                                            + str(clistAb2[aB2])+' and i. '
                                                            + str(secondAb+1)
                                                            + ' and n. CA'), 1))
                            # print(str(clistAb1[aB1])+':'+str(firstAb+1))
                            # print(str(clistAb2[aB2])+':'+str(secondAb+1))

        
                            totalRuns = totalRuns+1

                            if float(cAlpha) < float(calphaCutoff):

                            # if (totalRuns % 1500) <= 0:
                            #     print("Good Values  " + str(goodRuns)
                            #           + '\n'
                            #           + "Total Runs " + str(totalRuns))
                            # goodRuns = goodRuns + 1
                                columnOne = str(clistAb1[aB1])+':'+myresNumber1+':'+myresName1
                                columnTwo = str(clistAb2[aB2])+':'+myresNumber2+':'+myresName2
                                final.extend([columnOne, placeHolder, columnTwo,
                                              cAlpha])
                                os.chdir("..")
                                csvwriter.writerow(final)
                                os.chdir("pdbFiles")
                            else:
                                continue
                    tF = time.time()
                    print('Run Time = '+str((tF - tS)/60))
                    totalTime = totalTime+((tF-tS)/60)

                            
        
            t1 = time.time()
            tTime = ((t1-t0)/60)
            # print("Total Time = "+str(tTime))
            cmd.delete(noExt2[0])
        noExt3=dirlist[loadfirst].split(".")
        cmd.delete(noExt3[0])
print('Elapsed Time = '+str(round(totalTime, 2))+' minutes')
