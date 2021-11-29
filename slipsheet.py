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
    count = 0
    sortCodeIndex = 0
    add1Index = 0
    lines = fIn.readlines()
    for field in lines[0].split('\t'):
        if(field == 'Dt LH Sort Code'):
            sortCodeIndex = count
        if(field == 'Address Line 1'):
            add1Index = count
        count += 1
    newLines.append(f"{lines[0].strip()}{chr(9)}MediaSelect{chr(10)}")
    lineCount = 0
    sortBreak = False
    sortTitle = ''

    for line in lines:
        if(lineCount > 0):
            previousCode = lines[lineCount -
                                 1].split('\t')[sortCodeIndex].split('_')
            currentCode = line.split('\t')[sortCodeIndex].split('_')
            if(previousCode.__len__() == 7):
                sc0 = SortCode(
                    previousCode[1], previousCode[2], previousCode[4], previousCode[5])
            elif(previousCode.__len__() == 6):
                sc0 = SortCode(
                    previousCode[0], previousCode[1], previousCode[3], previousCode[4])
            else:
                sc0 = SortCode('xOTHER', '', '', 'INT')
            if(currentCode.__len__() == 7):
                sc1 = SortCode(
                    currentCode[1], currentCode[2], currentCode[4], currentCode[5])
            elif(currentCode.__len__() == 6):
                sc1 = SortCode(
                    currentCode[0], currentCode[1], currentCode[3], currentCode[4])
            else:
                sc1 = SortCode('xOTHER', '', '', 'INT')

            match   sc1.type:
                case 'A' if(sc1.type != sc0.type or sc1.bsp != sc0.bsp):
                    sortBreak = True
                    sortTitle = f'Area break: {sc1.bsp}'
                case 'P' if(sc1.type != sc0.type or sc1.postcode != sc0.postcode):
                    sortBreak = True
                    sortTitle = f'Postcode break: {sc1.postcode}'
                case 'R' if(sc1.type != sc0.type or sc1.state != sc0.state):
                    sortBreak = True
                    sortTitle = f'Residue: {sc1.state}'
                case 'INT' if(sc1.type != sc0.type):
                    sortBreak = True
                    sortTitle = 'INTERNATIONAL'
                case _:
                    sortBreak = False
            if(sortBreak):
                sortBreakLine = ''
                for x in range(count):
                    if(x == add1Index):
                        sortBreakLine += sortTitle
                    else:
                        sortBreakLine += '\t'
                newLines.append(f'{sortBreakLine}{chr(9)}SortBreak{chr(10)}')
            newLines.append(f"{line.strip()}{chr(9)}{chr(10)}")

        lineCount += 1

with open(fileName.replace('.txt','_slipsheet.txt'), 'a') as fOut:
    fOut.writelines(newLines)
