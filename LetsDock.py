import sys, os, shutil
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
#import tkinter, tkconstants, tkFileDialog

yORn=input("Are your files in this current directory? ")
if yORn=="no":
    print("Pick the directory" )
    theredirectory = askdirectory()
    os.chdir(theredirectory)
    
    lig_arr = [s for s in os.listdir('.') if s.endswith('.pdb')]
    print(lig_arr)
   
    print("Pick a receptor")
    receptor=askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdb files","*.pdb"),("all files","*.*")))
    
    print("Pick a ligand")
    ligand=askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdb files","*.pdb"),("all files","*.*")))
    
    rChain=input("Receptor chains, seperate by space. ")
    lChain=input("Ligand chains, seperate by space. ")
    textR=str(receptor)
    textL=str(ligand)

    os.system("cluspro_submit --ligand "+str(ligand)+" --receptor " +str(receptor)+ " --lig-chains "+'"'+str(lChain)+'"'+" --rec-chains  "+str(rChain)+ " -j "+str(textL)+"_docking_"+str(textR))
#########################################################     
if yORn=="yes":
    lig_arr = [s for s in os.listdir('.') if s.endswith('.pdb')]
    print (lig_arr)
    
    print("Pick a receptor")
    receptor=askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdb files","*.pdb"),("all files","*.*")))
    
    print("Pick a ligand")
    ligand=askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdb files","*.pdb"),("all files","*.*")))
    
    rChain=input("What is the receptor chains, seperate by space")
    lChain=input("What is the ligand chains, seperate by space")
    textR=str(receptor)
    textL=str(ligand)

    os.system("cluspro_submit --ligand "+str(ligand)+" --receptor " +str(receptor)+ " --lig-chains "+'"'+str(lChain)+'"'+" --rec-chains  "+str(rChain)+ " -j "+str(textL)+"_docking_"+str(textR))
        
