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

import logging






''' Will be using mixedCaps style '''

os.system('rm -rf pdbFiles')
os.system('rm calphaLog.log')
logging.basicConfig(filename='calphaLog.log', level=logging.DEBUG)
# launch pymol without gui
pymol.finish_launching(['pymol', '-c'])

t0 = time.time()
destfile = "output.csv"

# clistAb1 = ['H', 'L']
# clistAb2 = ['M', 'N']
calphaCutoff = str(round(4))
logging.info('cAlpha Cutoff = '+str(calphaCutoff)+'\n')

os.system("mkdir pdbFiles")
cmd.load("5_ab_test.mae")
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
    ab = fullList[x].split('_united')[0]
    ab = ab.split('t.')[1]
    # print(ab)


    cmd.save(os.getcwd() + '/pdbFiles/' + ab + '.pdb', fullList[x])


# print("PDB files generated!")

cmd.reinitialize()
os.chdir("pdbFiles")
dirlist = os.listdir(".")
dirlist = sorted(dirlist)
os.chdir("..")
secondStart = 0

final = []




# making the titles
titleList = ['Antibody 1', ' ', 'Antibody 2', 'cAlpha', 'centRoid', 'MinDistance']

# for the loop counter
totalRuns = 0
goodRuns = 0


overallTime = time.time();
#totalres = int(len(stored.residues1))*int(len(stored.residues2))

# Opening CSV file for writting.
with open(destfile, 'wb') as csvfile:
    os.chdir('pdbFiles')
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(titleList)
    for loadfirst in range(0,len(dirlist)):


        cmd.load(dirlist[loadfirst])
        abTemp=(cmd.get_object_list('all'))
        noExt1 = dirlist[loadfirst].split('.pdb')
        # print(noExt1[0])
        cmd.alter(str(noExt1[0])+' and chain H', 'chain = "'+str(noExt1[0])+'.H"')
        cmd.alter(str(noExt1[0])+' and chain L', 'chain = "'+str(noExt1[0])+'.L"')
        renumber.renumber('chain ' + str(noExt1[0]) + '.H', 1)
        renumber.renumber('chain ' + str(noExt1[0]) + '.L', 1)

        clistAb1 = cmd.get_chains()
        # print(clistAb1)
        secondStart = secondStart + 1


        for loadsecond in range(secondStart,len(dirlist)):

            cmd.load(dirlist[loadsecond])
            noExt2 = dirlist[loadsecond].split('.pdb')
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
                    tS = time.time()
                    print(str(clistAb1[aB1])+' : '+str(clistAb2[aB2]))
                    logging.info(str(clistAb1[aB1])+' : '+str(clistAb2[aB2]))
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

                            # starttime = time.time();
                            myresName1 = (stored.resN1[firstAb])
                            myresNumber1 = (stored.residues1[firstAb])
                            myresName2 = (stored.resN2[secondAb])
                            myresNumber2 = (stored.residues2[secondAb])
                            placeHolder = ' '
                            # cAlpha Calculation
                            cAlpha = str(round(cmd.distance('output', 'chain '
                                                            + str(clistAb1[aB1])
                                                            + ' and i. ' + str(firstAb+1)
                                                            + ' and n. CA', 'chain '
                                                            +str(clistAb2[aB2])+' and i. '
                                                            + str(secondAb+1)
                                                            + ' and n. CA'), 1))
                            # totalRuns = totalRuns+1
                            if float(0) < float(cAlpha) < float(calphaCutoff):
                                centRoid = str(round(cmd.distance('output', 'chain ' + str(
                                    clistAb1[aB1]) + ' and i. '
                                                                  + str(firstAb + 1),
                                                                  'chain ' + str(
                                                                      clistAb2[aB2]) + ' and i. '
                                                                  + str(secondAb + 1), -1, 4), 1))
                                extra = ""

                                sel1 = 'chain ' + str(clistAb1[aB1]) + ' and i. ' + str(
                                    firstAb + 1)
                                sel2 = 'chain ' + str(clistAb2[aB2]) + ' and i. ' + str(
                                    secondAb + 1)
                                max_dist = '10'
                                # builds models
                                m1 = cmd.get_model(
                                    sel2 + " around " + str(max_dist) + " and " + sel1 + extra)
                                m1o = cmd.get_object_list(sel1)
                                m2 = cmd.get_model(
                                    sel1 + " around " + str(max_dist) + " and " + sel2 + extra)
                                m2o = cmd.get_object_list(sel2)

                                # defines selections
                                cmd.select("__tsel1a",
                                           sel1 + " around " + str(
                                               max_dist) + " and " + sel2 + extra)
                                cmd.select("__tsel1", "__tsel1a and " + sel2 + extra)
                                cmd.select("__tsel2a",
                                           sel2 + " around " + str(
                                               max_dist) + " and " + sel1 + extra)
                                cmd.select("__tsel2", "__tsel2a and " + sel1 + extra)
                                cmd.select("IntAtoms_" + max_dist, "__tsel1 or __tsel2")
                                cmd.select("IntRes_" + max_dist, "byres IntAtoms_" + max_dist)

                                s = ""
                                counter = 0
                                atomlist = []
                                for c1 in range(len(m1.atom)):
                                    for c2 in range(len(m2.atom)):
                                        distance = math.sqrt(sum(map(lambda f: (f[0] - f[1]) ** 2,
                                                                     zip(m1.atom[c1].coord,
                                                                         m2.atom[c2].coord))))
                                        if distance < float(max_dist):
                                            # s += "%s/%s/%s/%s/%s to %s/%s/%s/%s/%s: %.3f\n" % (
                                            #     m1o[0], m1.atom[c1].chain, m1.atom[c1].resn,
                                            #     m1.atom[c1].resi, m1.atom[c1].name, m2o[0],
                                            #     m2.atom[c2].chain, m2.atom[c2].resn,
                                            #     m2.atom[c2].resi,
                                            #     m2.atom[c2].name, distance)
                                            counter += 1
                                        atomlist.append(distance)
                                        finList = round(min(atomlist), 1)



                                goodRuns = goodRuns + 1

                                columnOne = str(clistAb1[aB1])+':'+myresNumber1+':'+myresName1
                                columnTwo = str(clistAb2[aB2])+':'+myresNumber2+':'+myresName2

                                final.extend([columnOne, placeHolder, columnTwo,
                                              cAlpha, centRoid, finList])


                                csvwriter.writerow(final)
                            else:
                                pass
                    tF = time.time()
                    runTime = 'Run Time = ' + str((tF - tS) / 60)
                    print(runTime)
                    logging.info(runTime)
                    goodValues = "Good Values  " + str(goodRuns)
                    print(goodValues)
                    logging.info(goodValues+'\n')
                    totalTime = totalTime + ((tF - tS) / 60)
            t1 = time.time()
            tTime = ((t1 - t0) / 60)


            cmd.delete(noExt2[0])
        noExt3 = dirlist[loadfirst].split(".pdb")
        cmd.delete(noExt3[0])

elapsedTime = 'Elapsed Time = ' + str(round(totalTime, 2)) + ' minutes'
print(elapsedTime)
logging.info(elapsedTime)









