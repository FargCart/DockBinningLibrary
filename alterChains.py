import os
from pymol import cmd
import pymol
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import renumber


pymol.finish_launching(['pymol', '-c'])

cmd.reinitialize()
allmyChains = []
theirDir = askdirectory()
os.chdir(theirDir)
dirlist = os.listdir('.')
dirlist = sorted(dirlist)

for mstart in range(0,len(dirlist)):
    cmd.load(dirlist[mstart])
    abtemp = (cmd.get_object_list('all'))
    noExt1 = dirlist[mstart].split('.pdb')
    shortname = dirlist[mstart].split('.pdb')
    print(shortname)
    cmd.alter(str(shortname[0])+' and chain H', 'chain = "'+str(noExt1[0])+'.H"')
    cmd.alter(str(shortname[0])+' and chain L', 'chain = "'+str(noExt1[0])+'.L"')
    renumber.renumber('chain ' + str(noExt1[0]) + '.H', 1)
    renumber.renumber('chain ' + str(noExt1[0]) + '.L', 1)

    currentChains = cmd.get_chains(shortname[0])
    allmyChains.append(currentChains)

print(allmyChains)


