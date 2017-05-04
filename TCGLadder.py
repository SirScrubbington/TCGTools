#!usr/bin/env python
import pickle
import os
import operator
import sys

class Player():
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.wins = 0
        self.losses = 0
        self.history = []

    def add_game(self,str):
        self.history.append(str)

    def get_history(self):
        return self.history

    def get_elo(self):
        return self.elo

    def get_name(self):
        return self.name

    def get_wins(self):
        return self.wins

    def get_games(self):
        return self.wins + self.losses

    def get_losses(self):
        return self.losses

    def __hash__(self):
        return hash(self.elo)

    def __lt__(self,other):
        return self.elo < other.elo

    def __gt__(self,other):
        return self.elo > other.elo

    def __eq__(self,other):
        return self.hash() == other.hash()

    def __ne__(self,other):
        return not self.__eq__(self,other)

def startup():
    if os.path.isfile("TCG_Ladder.lad"):
        data = pickle.load(open("TCG_Ladder.lad", "rb"))
    else:
        data = {}
        pickle.dump(data, open("TCG_Ladder.lad", "wb"))
    return data


def saveData(data):
    pickle.dump(data, open("TCG_Ladder.lad", "wb"))


def addPlayer(data):
    name = input("Name: ")
    player = Player(name)
    data[name] = player
    saveData(data)
    return data

def removePlayer(data):
    name = input("Name: ")
    del data[name]
    saveData(data)
    return data

def Battle(p1, p2, k):
    elo1 = p1.elo
    elo2 = p2.elo

    if p1.get_games() != 0:
        print(p1.get_games())
        k1 = k / p1.get_games()
    else:
        k1 = k

    if p2.get_games() != 0:
        k2 = k / p2.get_games()
    else:
        k2 = k

    exp1 = expected(elo1,elo2)
    exp2 = expected(elo2,elo1)

    p1change = round(elo(elo1,exp1,1,k))
    p2change = round(elo(elo2,exp2,0,k))

    if p1change < 500:
        p1change = 500
    if p2change < 500:
        p2change = 500

    p1.add_game(('w',p2.name,p1change-p1.elo,p1change))
    p2.add_game(('l',p1.name,p2change-p2.elo,p2change))

    p1.elo = p1change
    p2.elo = p2change
    p1.wins += 1
    p2.losses += 1
    return 0

def expected(A, B):
    """
    Calculate expected score of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, k=32):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    return old + k * (score - exp)

def printStats(data,sortmethod):

    # Sort Alphabetically
    if sortmethod == 0:
        a = list(data.keys())
        a.sort()
        for i in a:
            print(data[i].name, "-", data[i].elo, "-", data[i].get_games(), 'games played')
        if len(data) == 0:
            print("No data")
        pass

    # Sort by ELO
    if sortmethod == 1:
        a = []
        for k, v in data.items():
            a.append((v.elo,v.name,v.wins,v.losses))
            a.sort(reverse=True)
        c = 0
        for i in a:
            c+=1
            if i[2]+i[3] > 0:
                sys.stdout.write(str(c)+": "+str(i[1])+" "+str(i[0])+" " + "{0:.2f}".format(i[2]/(i[2]+i[3])) + " Games: "+str(i[2]+i[3])+" ("+str(i[2])+"-"+str(i[3])+")\n")
            else:
                sys.stdout.write(str(c)+": "+str(i[1])+" "+str(i[0])+" " + "{0:.2f}".format(i[2]/(1)) + " Games: "+str(i[2]+i[3])+" ("+str(i[2])+"-"+str(i[3])+")\n")

def printhistory(data):
    name = input("Name: ")
    p = data[name]
    h = p.get_history()
    sys.stdout.write("Rating initialised at 1000")
    for i in h:
        if i[0]=='l':
            sys.stdout.write("Loss against "+str(i[1])+", Rating: "+str(i[3])+" ("+str(i[2])+")\n")
        elif i[0]=='w':
            sys.stdout.write("Win against " + str(i[1]) + ", Rating: "+str(i[3])+" (+"+str(i[2])+")\n")

    pass

def MainLoop(data):
    loop = True
    while loop == True:
        print()
        print()
        print()
        print("What would you like to do?")
        print("""0 - Exit
1 - Print Stats
2 - Record a Bo1 Match
3 - Record a Bo3 Match (2-0)
4 - Record a Bo3 Match (2-1)
5 - Add a player
6 - Remove a player
7 - Check player history""")
        action = input("Please enter the corresponing number: ")
        if action == "0":
            quit()
        elif action == "1":
            printStats(data,1)
        elif action == "2":
            if len(data) > 1:
                p1 = input("Winner's name: ")
                p2 = input("Loser's name: ")

                exit = False

                if p1 not in data:
                    sys.stdout.write("Player '" + p1 + "' does not exist.\n")
                    exit = True

                if p2 not in data:
                    sys.stdout.write("Player '" + p2 + "' does not exist.\n")
                    exit = True

                if exit == True:
                    sys.stdout.write("Please add the missing users and try again.\n")
                else:
                    Battle(data[p1], data[p2], 32)
                    saveData(data)
            else:
                print("Not enough people")

        elif action == "3":
            if len(data) > 1:
                p1 = input("Winner's name: ")
                p2 = input("Loser's name: ")

                exit = False

                if p1 not in data:
                    sys.stdout.write("Player '" + p1 + "' does not exist.\n")
                    exit = True

                if p2 not in data:
                    sys.stdout.write("Player '" + p2 + "' does not exist.\n")
                    exit = True

                if exit == True:
                    sys.stdout.write("Please add the missing users and try again.\n")
                else:
                    Battle(data[p1], data[p2], 32)
                    Battle(data[p1], data[p2], 32)
                    saveData(data)
            else:
                print("Not enough people")

        elif action == "4":
            if len(data) > 1:
                p1 = input("Winner's name: ")
                p2 = input("Loser's name: ")

                exit = False

                if p1 not in data:
                    sys.stdout.write("Player '" + p1 + "' does not exist.\n")
                    exit = True

                if p2 not in data:
                    sys.stdout.write("Player '" + p2 + "' does not exist.\n")
                    exit = True

                if exit == True:
                    sys.stdout.write("Please add the missing users and try again.\n")
                else:
                    Battle(data[p1], data[p2], 32)
                    Battle(data[p1], data[p2], 32)
                    saveData(data)
            else:
                print("Not enough people")

        elif action == "5":
            addPlayer(data)
        elif action == "6":
            removePlayer(data)
        elif action == "7":
            printhistory(data)

data = startup()
MainLoop(data)


