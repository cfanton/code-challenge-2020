class Posto:
    def __init__(self,x,y,freeSeat,D_or_PM):
        self.x = x
        self.y = y
        self.freeSeat = freeSeat
        self.D_or_PM = D_or_PM
        self.score=0

class Developer():
    def __init__(self, company: str, bonus: int, skills):
        self.company = company
        self.bonus = bonus
        self.skills = skills
        self.x = 0
        self.y = 0
        self.free=True

class Manager():
    def __init__(self, company: str, bonus: int):
        self.company = company
        self.bonus = bonus
        self.x = 0
        self.y = 0
        self.free=True

def createMatrixOfPosti(seats):

    matrixOfPosti = []

    j = 1
    for lineOfSeats in seats:
        listOfPosti = []
        i = 1
        for seat in lineOfSeats:
            if seat == '_':
                listOfPosti.append(Posto(i, j, True, "D"))
            elif seat == 'M':
                listOfPosti.append(Posto(i, j, True, "PM"))
            else:
                listOfPosti.append(Posto(0, 0, False, ""))
            i = i + 1
        j = j + 1
        matrixOfPosti.append(listOfPosti)

    return matrixOfPosti


def allocatePostiToPeople(matrixOfPosti, listOfDevelopers, listOfManagers):

    j=1
    for listOfSeats in matrixOfPosti:
        i=1
        for posto in listOfSeats:
            if posto.freeSeat==True:
                if posto.D_or_PM=="D":
                    for developer in listOfDevelopers:
                        if developer.free==True:
                            developer.free=False
                            developer.x = i
                            developer.y = j
                            posto.freeSeat=False
                elif posto.D_or_PM=="PM":
                    for manager in listOfManagers:
                        if manager.free==True:
                            manager.free=False
                            manager.x = i
                            manager.y = j
                            posto.freeSeat=False
            i=i+1
        j=j+1

    return matrixOfPosti, listOfDevelopers, listOfManagers



def main():
    seats = [['#', '#', '#', '#', '#'], ['#', '_', '#', '#', '_'], ['#', 'M', 'M', '_', '_']]
    listOfDevelopers=[[],[]]
    listOfManagers=[[],[]]

    # create matrix of posti
    matrixOfPosti = createMatrixOfPosti(seats)

    # allocate posti to people
    matrixOfPosti, listOfDevelopers, listOfManagers = allocatePostiToPeople(matrixOfPosti,listOfDevelopers, listOfManagers)