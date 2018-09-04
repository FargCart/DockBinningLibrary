import os
##nfile=input('What is the maegz file you want to run (not including extension)? ')
##chain1=input('What are the chains of the first structure? ')
##chain2=input('What are the chains of the second strucuture? ')
nfile=("DL11_Docking_gD2_285-out")
chain1=("A")
chain2=("H,L")

os.system("$schrodinger/run protein_interaction_analysis.py -structure "+(nfile)+".maegz"+ " -group1 "+(chain1)+ " -group2 "+(chain2)+" -outfile "+ (nfile)+"_interaction_tables.csv")
