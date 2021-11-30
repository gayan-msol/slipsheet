import os

fileName = input("Sorted File:")
newLines = []

class SortCode:
    def __init__(self, state, bsp, postcode, type):
        self.bsp = bsp
        self.postcode = postcode
        self.state = state
        self.type = type

with open(fileName.replace('"', ''), "r") as fIn:
    fieldCount = 0
    sortCodeIndex = 0
    add1Index = 0
    isLineHaul = False
    lines = fIn.readlines()
    delimeter = '\t'
    if(lines[0].split(',').__len__() > lines[0].split('\t').__len__()):
        delimeter = ','
    for field in lines[0].split(delimeter):
        match field:
            case 'Dt LH Sort Code':
                sortCodeIndex = fieldCount
                isLineHaul = True
            case 'Dt PP Sort Code':
                sortCodeIndex = fieldCount
            case 'Address Line 1':
                add1Index = fieldCount
        fieldCount += 1
    newLines.append(f"{lines[0].strip()}{chr(9)}MediaSelect{chr(10)}")
    lineCount = 0
    sortBreak = False
    sortTitle = ''

    for line in lines:
        if(lineCount > 0):
            previousCode = lines[lineCount -1].split(delimeter)[sortCodeIndex].split('_')
            currentCode = line.split(delimeter)[sortCodeIndex].split('_')
            if(previousCode.__len__() < 4):
                sc0 = SortCode('xOTHER', '', '', 'INT')                
            elif(isLineHaul):
                sc0 = SortCode(previousCode[1], previousCode[2], previousCode[4], previousCode[5])                
            else:
                sc0 = SortCode(previousCode[0], previousCode[1], previousCode[3], previousCode[4])

            if(currentCode.__len__() < 4):
                sc1 = SortCode('xOTHER', '', '', 'INT')                
            elif(isLineHaul):
                sc1 = SortCode(currentCode[1], currentCode[2], currentCode[4], currentCode[5])                
            else:
                sc1 = SortCode(currentCode[0], currentCode[1], currentCode[3], currentCode[4])    

            match   sc1.type:
                case 'A' if(sc1.type != sc0.type or sc1.bsp != sc0.bsp):
                    sortBreak = True
                    sortTitle = f'Area Direct - {sc1.bsp}'
                case 'P' if(sc1.type != sc0.type or sc1.postcode != sc0.postcode):
                    sortBreak = True
                    sortTitle = f'Postcode Direct - {sc1.postcode}'
                case 'R' if(sc1.type != sc0.type or sc1.state != sc0.state):
                    sortBreak = True
                    sortTitle = f'Residue - {sc1.state}'
                case 'INT' if(sc1.type != sc0.type):
                    sortBreak = True
                    sortTitle = 'INTERNATIONAL'
                case _:
                    sortBreak = False
            if(sortBreak):
                sortBreakLine = ''
                for x in range(fieldCount):
                    if(x == add1Index):
                        sortBreakLine += sortTitle
                    else:
                        sortBreakLine += delimeter
                newLines.append(f'{sortBreakLine}{delimeter}Sort Break{chr(10)}')
            newLines.append(f"{line.strip()}{delimeter}{chr(10)}")
        lineCount += 1

with open(fileName.replace('.txt','_slipsheet.txt'), 'a') as fOut:
    fOut.writelines(newLines)
