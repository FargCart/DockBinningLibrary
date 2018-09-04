import os


os.system("$schrodinger/run protein_interaction_analysis.py -structure 5_ab_control.maegz -group1 A,B -group2 C,D,E,F,G,H,I,J -outfile 00_vs_all.csv")
os.system("$schrodinger/run protein_interaction_analysis.py -structure 5_ab_control.maegz -group1 C,D -group2 E,F,G,H,I,J -outfile 05_vs_all.csv")
os.system("$schrodinger/run protein_interaction_analysis.py -structure 5_ab_control.maegz -group1 E,F -group2 G,H,I,J -outfile 25_vs_all.csv")
os.system("$schrodinger/run protein_interaction_analysis.py -structure 5_ab_control.maegz -group1 G,H -group2 I,J -outfile 04_vs_all.csv")
