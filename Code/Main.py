import os
import time


class Posto:
    def __init__(self, x, y, freeSeat, D_or_PM):
        self.x = x
        self.y = y
        self.freeSeat = freeSeat
        self.D_or_PM = D_or_PM
        self.score = 0


class Developer():
    def __init__(self, company: str, bonus: int, skills):
        self.company = company
        self.bonus = bonus
        self.skills = skills
        self.x = 0
        self.y = 0
        self.free = True


class Manager():
    def __init__(self, company: str, bonus: int):
        self.company = company
        self.bonus = bonus
        self.x = 0
        self.y = 0
        self.free = True


def createMatrixOfPosti(seats):
    matrixOfPosti = []

    j = 0
    for lineOfSeats in seats:
        listOfPosti = []
        i = 0
        for seat in lineOfSeats:
            if seat == '_':
                listOfPosti.append(Posto(i, j, True, "D"))
            elif seat == 'M':
                listOfPosti.append(Posto(i, j, True, "PM"))
            else:
                listOfPosti.append(Posto(-1, -1, False, ""))
            i = i + 1
        j = j + 1
        matrixOfPosti.append(listOfPosti)

    return matrixOfPosti


def allocatePostiToPeople(matrixOfPosti, listOfDevelopers, listOfManagers):
    # listOfDevelopers.sort(key=lambda x: x.company, reverse=True)
    # listOfManagers.sort(key=lambda x: x.company, reverse=True)
    listOfDevelopers.sort(key=lambda x: x.company, reverse=False)
    listOfManagers.sort(key=lambda x: x.company, reverse=False)

    j = 0
    for listOfSeats in matrixOfPosti:
        i = 0
        for posto in listOfSeats:
            if posto.freeSeat == True:
                if posto.D_or_PM == "D":
                    for developer in listOfDevelopers:
                        # NB: il vincolo corretto è >=1 e <=100
                        if developer.free == True and len(developer.skills) >= 1 and len(developer.skills) <= 100:
                            developer.free = False
                            developer.x = i
                            developer.y = j
                            posto.freeSeat = False
                            break
                elif posto.D_or_PM == "PM":
                    for manager in listOfManagers:
                        if manager.free == True:
                            manager.free = False
                            manager.x = i
                            manager.y = j
                            posto.freeSeat = False
                            break
            i = i + 1
        j = j + 1

    return matrixOfPosti, listOfDevelopers, listOfManagers


def parse_file(filepath):
    matrix = []
    developers, managers = [], []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        index = 0
        w, h, dev_count, manager_count = 0, 0, 0, 0
        for line in lines:
            if index == 0:
                values = line.split()
                w = int(values[0])
                h = int(values[1])
            # parse MATRIX char
            if 0 < index < h + 1:
                line = line.replace("\n", "")
                row = []
                for char in line:
                    row.append(char)
                matrix.append(row)
            # parse DEVELOPERS
            elif index == h + 1:
                dev_count = int(line.replace("\n", ""))
                print("found " + str(dev_count))
            elif h + 1 < index <= h + dev_count + 1:
                line = line.replace("\n", "")
                values = line.split()
                company = values[0]
                bonus = int(values[1])
                skill_count = int(values[2])
                skills = []
                for i in range(0, skill_count):
                    s = values[2 + i + 1]
                    skills.append(s)
                skills = skills
                developer = Developer(company, bonus, skills)
                developers.append(developer)
            # parse MANAGERS
            elif index == h + dev_count + 2:
                manager_count = int(line.replace("\n", ""))
                print("found " + str(manager_count))
            elif h + dev_count + 2 < index <= h + dev_count + manager_count + 2:
                line = line.replace("\n", "")
                values = line.split()
                company = values[0]
                bonus = int(values[1])
                manager = Manager(company, bonus)
                managers.append(manager)
            index += 1
    f.close()

    print(w)
    print(h)
    print(len(matrix))
    print(len(developers))
    print(len(managers))
    return w, h, matrix, developers, managers


def writeToFile(filepath, listOfDevelopers, listOfManagers):
    if os.path.exists(filepath):
        os.remove(filepath)

    time.sleep(5)

    f = open(filepath, "a")
    for dev in listOfDevelopers:
        if dev.free == False:
            # print(str(dev.x))
            # print(str(dev.y))
            f.write(str(dev.x) + " " + str(dev.y) + "\n")
        else:
            f.write("X" + "\n")

    for manager in listOfManagers:
        if manager.free == False:
            f.write(str(manager.x) + " " + str(manager.y) + "\n")
        else:
            f.write("X" + "\n")
    f.close()
    print("file written!")


def main():
    # seats = [['#', '#', '#', '#', '#'], ['#', '_', '#', '#', '_'], ['#', 'M', 'M', '_', '_']]
    # listOfDevelopers=[[],[]]
    # listOfManagers=[[],[]]

    # read input file
    in_file = "a_solar"
    w, h, seats, listOfDevelopers, listOfManagers = parse_file("input\\" + in_file + ".txt")

    # create matrix of posti
    matrixOfPosti = createMatrixOfPosti(seats)

    # allocate posti to people
    matrixOfPosti, listOfDevelopers, listOfManagers = allocatePostiToPeople(matrixOfPosti, listOfDevelopers,
                                                                            listOfManagers)

    # write output file
    writeToFile("output\\" + in_file + "_output.txt", listOfDevelopers, listOfManagers)


if __name__ == "__main__":
    main()
