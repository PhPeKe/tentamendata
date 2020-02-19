import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt

data = pd.read_excel("data/ttm.xlsx")

# jaar variable
data["year"] = [int(x.year) for x in data["Tentamendatum"]]
# warning flag voor meer dan 1 parallel tentamen Y for tentamen X
data["parallel>1"] = 0
# lag variable
data["lag"] = 999

#  welke vakken in dezelfde periode zitten (var Periode) en binnen een jaar (uit Tentamendatum)
tegelijkertijd = {}
for year in set(data["year"]):
    tegelijkertijd[year] = {}
    for periode in set(data["Periode"]):
        tegelijkertijd[year][periode] = {}
        vakken_zelfde_periode_jaar = data.loc[data["Periode"] == periode].loc[data["year"] == year]
        # list studenten per vak
        studenten_per_vak = {vak: vakken_zelfde_periode_jaar.loc[vakken_zelfde_periode_jaar["RES_Module_code"] == vak][
            "INS_Studentnummer"] for vak in set(vakken_zelfde_periode_jaar["RES_Module_code"])}
        # tegelijk door dezelfde studenten zijn gedaan (itertools.combinations geeft alle unieke combinaties)
        tentamen_X = []
        for vak1, vak2 in itertools.combinations(studenten_per_vak.keys(), 2):
            n_vak1 = len(studenten_per_vak[vak1])
            n_vak2 = len(studenten_per_vak[vak2])
            n_overlap = len(set(studenten_per_vak[vak1]) & set(studenten_per_vak[vak2]))
            smallest = n_vak1 if n_vak1 < n_vak2 else n_vak2
            print("")
            print("------------------------------")
            print("N students " + vak1 + " " + str(n_vak1))
            print("N students " + vak2 + " " + str(n_vak2))
            print("N overlap " + str(n_overlap))
            print("------------------------------")
            if n_overlap > 20 and n_overlap > smallest / 2:
                print("!!! added " + str(vak1) + " and " + str(vak2) + " with overlap " + str(n_overlap))
                print("Data Info:")
                date_vak1 = list(set(
                    vakken_zelfde_periode_jaar.loc[vakken_zelfde_periode_jaar["RES_Module_code"] == vak1][
                        "Tentamendatum"]))[0]
                date_vak2 = list(set(
                    vakken_zelfde_periode_jaar.loc[vakken_zelfde_periode_jaar["RES_Module_code"] == vak2][
                        "Tentamendatum"]))[0]
                print(date_vak1)
                print(date_vak2)
                # Als X eerst was, zou er bij “lag” het aantal dagen verschil, in negatief, moeten
                # Als X het latere tentamen was, zou bij  “lag” het aantal dagen verschil, positief, moeten komen.
                lag = (date_vak1 - date_vak2).days
                print("Tijd tussen " + str(vak1) + " en " + str(vak2) + ": " + str(lag) + " dagen")
                tegelijkertijd[year][periode][vak1 + " " + vak2] = {"averlap": n_overlap,
                                                                    "lag": lag,
                                                                    "date vak1": date_vak1,
                                                                    "date vak2": date_vak2}
            print("")
    # break
# break
"""
# Checken of tentamen X of Y al in de lijst staat (meer dan een dubbele rostering)
# Als het zo is, vervang met de hoogste overlap en maak warning flag voor het andere tentamen
if vak1 in tentamen_X:
	print(str(vak1) + " staat dubbel in de lijst met")
if vak2 in tentamen_X:
	pass
tentamen_X.append(vak1)
tentamen_X.append(vak2)
"""
