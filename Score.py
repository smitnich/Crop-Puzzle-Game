import Globals

score = 0
score_mult = 10
combo_mult = 1

def Reset_Score():
    global score
    Globals.update_score = True
    score = 0
    Reset_Combo()

def Get_Score():
    global score
    return score

def Reset_Combo():
    global combo_mult
    Globals.update_score = True
    combo_mult = 1

def Get_Combo():
    global combo_mult
    return combo_mult

def Add_Match(length):
    global score
    global combo_mult
    Globals.update_score = True
    score = score + length*score_mult*combo_mult
    combo_mult = combo_mult + 1