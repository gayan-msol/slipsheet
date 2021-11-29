import os

fileName = input("Sorted File:")
newLines = []

class SortCode:
    def __init__(self,state,bsp,postcode,type):
        
        self.bsp =bsp
        self.postcode=postcode
        self.state=state
        self.type =type


with open(fileName.replace('"',''), "r") as fIn:
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

    for line in lines:
        if(lineCount > 0):
            previousCode = lines[lineCount -1].split('\t')[sortCodeIndex]            
            currentCode = line.split('\t')[sortCodeIndex]
            sc0 = SortCode(previousCode[1],previousCode[2],previousCode[4],previousCode[5])
            sc1 = SortCode(currentCode[1],currentCode[2],currentCode[4],currentCode[5])

            if(currentCode != previousCode):
                codes = currentCode.split('_')
                sortBreakLine = ''
                for x in range(count):
                    if(x == add1Index):
                        if(codes[1] == 'xOTHER'):
                            sortBreakLine += 'INTERNATIONAL'
                        else:
                            match codes[5]:
                                case 'P':                            
                                    sortBreakLine += f'Postcode break: {codes[4]}'
                                case 'A':                            
                                    sortBreakLine += f'Area break: {codes[2]}'  
                                case 'R':                            
                                    sortBreakLine += f'Residue: {codes[1]}' 
                    else:
                        sortBreakLine += '\t'
                newLines.append(f'{sortBreakLine}{chr(9)}SortBreak{chr(10)}')                            
            newLines.append(f"{line.strip()}{chr(9)}{chr(10)}")            
        lineCount += 1
    
with open("testOut.txt",'a') as fOut:
    fOut.writelines(newLines)