def getAllId():
    file = open("Customers.txt", 'r')
    CutsomersList = []
    for x in file.readlines():
        line = x.split(" ")
        CutsomersList.append(line[0])
    return CutsomersList


def GetVolLat(id):
    file = open("Customers.txt", 'r')
    for x in file.readlines():
        line = x.split(" ")
        if line[0] == id:
            return line[4]


def delete_vol(id):
    file = open("Customers.txt", 'r')
    content = ""
    for x in file.readlines():
        line = x.split(" ")
        if line[0] != id:
            content += line + "\n"
    file.close()
    filew = open("Customers.txt", 'w')
    filew.write(content)

def GetVolLong(id):
    file = open("Customers.txt", 'r')
    for x in file.readlines():
        line = x.split(" ")
        if line[0] == id:
            return line[3]


def GetVolIP(id):
    file = open("Customers.txt", 'r')
    for x in file.readlines():
        line = x.split(" ")
        if line[0] == id:
            return line[2]


def Get_Distance(longitude, latitude, vol_longitude, vol_latitude):
    return (longitude - vol_longitude)*(longitude - vol_longitude) + (latitude - vol_latitude)*(latitude - vol_latitude)

def getRunning():
    file = open("running.txt", 'r')
    num = int(file.read())
    file.close()
    filew = open("running.txt", 'w')
    filew.write(str(num + 1))
    return num

def defrunning(num):
    filew = open("running.txt", 'w')
    listID = getAllId()
    newlist = []
    for i in range(0, len(listID) - 1):
        newlist.append( int(listID[i]))
    filew.write(str(max(newlist) + 1))