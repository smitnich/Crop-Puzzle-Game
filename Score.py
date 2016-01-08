import Globals

score = 0
score_mult = 10

def Reset_Score():
    global score
    Globals.update_score = True
    score = 0

def Get_Score():
    global score
    return score

def Add_Match(length):
    global score
    Globals.update_score = True
    score = score + length*score_mult