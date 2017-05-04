import os

savedir = os.path.dirname(os.path.realpath(__file__)) +'\decks\\'


print(savedir)

class Card:
    def __init__(self,name,set,no):
        self.name=name
        self.set=set
        self.no=no

    def __str__(self):
        return self.name + " " + str(self.set) + " " + str(self.no)

    def __repr__(self):
        return self.name + " " + str(self.set) + " " + str(self.no)

class Trainer(Card):
    def __init__(self,name,set,no):
        self.type="Trainer"
        Card.__init__(self,name,set,no)
        pass

class Pokemon(Card):
    def __init__(self,name,set,no):
        self.type = "Pokémon"
        Card.__init__(self, name, set, no)
        pass
class Energy(Card):
    def __init__(self,name,set,no):
        self.type = "Energy"
        Card.__init__(self, name, set, no)
        pass

class Deck:
    def __init__(self,name):
        self.name=name
        self.cards=[]
        self.format=[]
    def load(self,file):
        f = open(file,'r')
        splt = f.read().splitlines()
        for i in range(len(splt)):
            type = -1
            if "##Pokémon" in splt[i]:
                type=0
            elif "##Trainer Cards" in splt[i]:
                type=1
            elif "##Energy" in splt[i]:
                type=2
            if "**" in splt[i]:
                continue

            if "*" in splt[i]:
                temp=splt[i].split()
                count=temp[1]
                nam=str(temp[2:len(temp)-2])
                set=temp[len(temp)-2]
                num=temp[len(temp)-1]
                if type==0:
                    for i in range(0,count,1):
                        add=Pokemon(nam,set,num)
                        self.cards.append(add)
                        print(add)
                    pass
                elif type==1:
                    for i in range(0,temp[1],1):
                        print(str(i), str(temp[i]))
                        add=Trainer(nam,set,num)
                        self.cards.append(add)
                        print(add)
                    pass
                elif type==2:
                    for i in range(0,temp[1],1):
                        print(str(i), str(temp[i]))
                        add=Energy(nam,set,num)
                        self.cards.append(add)
                        print(add)
                    pass
                pass
            pass
        pass
    def prnt(self,file):
        pass

d = Deck("Decidueye-Vileplume")
d.load(savedir+"Mewtwo.txt")
print(d.cards)