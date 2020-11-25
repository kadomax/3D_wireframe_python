def getVertsFromString(line):
    tempstring = ' '.join(line.split())
    temp = tempstring.split()
    del temp[0]
    for i in range(len(temp)):
        temp[i] = float(temp[i])
    
    return temp

def getindFromString(line):
    tempstring = ' '.join(line.split())
    s = ''
    temp = []
    for i in range(0 , len(tempstring)):
        if tempstring[i] == ' ':
            j = i + 1
            while(tempstring[j] != '/'):
                s = s + tempstring[j]
                j+=1
            temp.append(s)
            s = ''
    
    for i in range(len(temp)):
        temp[i] = int(temp[i])
    return temp


def getVerts(path):
    temp = []
    verts = []
    with open(path , 'r') as f:
        for line in f:
            if line[0] == 'v' and line[1] == ' ':
                temp = getVertsFromString(line)
                verts.append(tuple(temp))
    return verts
            

def getIndices(path):
    temp = []
    indices = []
    with open(path , 'r') as f:
        for line in f:
            if line[0] == 'f':
                temp = getindFromString(line)
                for element in temp:
                    indices.append(element)
    return indices






