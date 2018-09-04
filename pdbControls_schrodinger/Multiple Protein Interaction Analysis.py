import os


##nfile=input('What is the maegz file you want to run (not including extension)? ')
##chain1=input('What are the chains of the first structure? ')
##chain2=input('What are the chains of the second strucuture? ')

lig_arr = [s for s in os.listdir('.') if s.endswith('.maegz')]
print (lig_arr)
Num=raw_input("How many files? ")
if 0<int(Num):
    print("Ok")
    Name1=raw_input("maegz file? ")
    Name2=raw_input("Chain 1? ")
    Name3=raw_input("Chain 2? ")

if 1<int(Num):
    Name4=raw_input("maegz file ? ")
    Name5=raw_input("Chain 1? ")
    Name6=raw_input("Chain 2? ")
if 2<int(Num):
    Name7=raw_input("maegz file ? ")
    Name8=raw_input("Chain 1? ")
    Name9=raw_input("Chain 2? ")
if 3<int(Num):
    Name10=raw_input("maegz file ? ")
    Name11=raw_input("Chain 1? ")
    Name12=raw_input("Chain 2? ")
        
if 4<int(Num):
    Name13=raw_input("maegz file ? ")
    Name14=raw_input("Chain 1? ")
    Name15=raw_input("Chain 2? ")
        

if 0<int(Num):
    os.system("$schrodinger/run protein_interaction_analysis.py -structure "+str(Name1)+".maegz"+ " -group1 "+str(Name2)+ " -group2 "+str(Name3)+" -outfile "+ str(Name1)+"_interaction_tables.csv")

if 1<int(Num):
    os.system("$schrodinger/run protein_interaction_analysis.py -structure "+str(Name4)+".maegz"+ " -group1 "+str(Name5)+ " -group2 "+str(Name6)+" -outfile "+ str(Name4)+"_interaction_tables.csv")

if 2<int(Num):
    os.system("$schrodinger/run protein_interaction_analysis.py -structure "+str(Name7)+".maegz"+ " -group1 "+str(Name8)+ " -group2 "+str(Name9)+" -outfile "+ str(Name7)+"_interaction_tables.csv")

if 3<int(Num):
    os.system("$schrodinger/run protein_interaction_analysis.py -structure "+str(Name10)+".maegz"+ " -group1 "+str(Name11)+ " -group2 "+str(Name12)+" -outfile "+ str(Name10)+"_interaction_tables.csv")

if 4<int(Num):
    os.system("$schrodinger/run protein_interaction_analysis.py -structure "+str(Name13)+".maegz"+ " -group1 "+str(Name14)+ " -group2 "+str(Name15)+" -outfile "+ str(Name13)+"_interaction_tables.csv")



