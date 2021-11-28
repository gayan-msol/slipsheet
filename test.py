newLines = []
with open("JOB 205964 OUTPUT FILE - All Records.txt") as fIn:
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
            previousSortCode = lines[lineCount -1].split('\t')[sortCodeIndex]            
            sortCode = line.split('\t')[sortCodeIndex]
            if(sortCode != previousSortCode):
                codes = sortCode.split('_')
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