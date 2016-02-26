#vcd-pwl maker
#A tool for parsing vcd file and make pwl file.
#By Steve M Song(stevemsong@yahoo.com)
#!/bin/python
import re,sys

if len(sys.argv) < 2:
    print('usage: vcd-pwl.py <vcd-file>')
    sys.exit(1)
    
#inputFile = open('tb_mult8X8.vcd','r')
inputFile = open(sys.argv[1],'r')
contentList = inputFile.readlines()
inputFile.close()

signals={}
parseValue=[]
def collectSignals():       #collects signals in a dictionary format
    print('Collecting data for these signals:')
    for i in range(len(contentList)):
        if contentList[i]==('$scope module dut $end\n'):
            while re.search(r'\$var wire \d+\s\S+\s([a-zA-Z]+\S*)\s(\[\S+\])?',contentList[i+1]):
                mo=re.search(r'\$var wire (\d+)\s(\S+)\s((\S+)(\s\[\S+\])?)',contentList[i+1])
                signals[mo.group(2)]=mo.group(3).replace(" ","")    #group(1)=bits, group(2)=key, group(3)=value
                i=i+1
    return signals

def timescale():        #reads in timescale
    for i in range(len(contentList)):
        if contentList[i]==('$timescale\n'):
            while contentList[i] != ('$end\n'):
                if re.search(r'\s+\d+(\w)s',contentList[i]):
                    timescale = re.search(r'\s+\d+(\w)s',contentList[i]).group(1)
                i=i+1
    return timescale

def printScreen():      #outputs signal transitions with timestamp
    for i in range(len(contentList)):
        if re.search(r'\#\d+',contentList[i]):
            print(re.search(r'\#\d+',contentList[i]).group() + timescale + 'sec')
        for k in signals.keys():
            if re.search(r'(^[01bx]{2,}\s|^[x01])'+re.escape(k)+'\n',contentList[i]):
                print(signals[k] + str('=>') + str(re.search(r'(^[01bx]{2,}\s|^[x01])'+re.escape(k)+'\n',contentList[i]).group(1).strip()))
                
def captureData():    #captures signal transition in a list format
    count=-1    #initialize count for dictionary length
    for k,j in signals.items():
        count=count+1    #counting the k,j loop iteration for parseValue.append purpose
        parseValue.append([j])
        for i in range(len(contentList)):
            if re.search(r'(^[01bx]{2,}\s|^[x01])'+re.escape(k)+'\n',contentList[i]):
                parseValue[count].append(re.search(r'(^[01bx]{2,}\s|^[x01])'+re.escape(k)+'\n',contentList[i]).group(1).strip()) #signal value append to list
                while re.search(r'^\#(\d+)\n',contentList[i]) == None:
                    i=i-1    
                    if re.search(r'^\#(\d+)\n',contentList[i]):
                        parseValue[count].append(re.search(r'^\#(\d+)\n',contentList[i]).group(1) + timescale)    #timestamp append to list
    return parseValue

def bus2bitConversion():    #converts bus in list to individual bit transition
    for i in range(len(mylist)):
        mo=re.search(r'([^\[]+)\[(\d+):0\]',mylist[i][0])
        if mo:
            for j in range(int(mo.group(2))+int(1)):
                mylist.append([mo.group(1)+str([j])])
    for i in range(len(mylist)):
        mbus=re.search(r'([^\[]+)\[(\d+):0\]',mylist[i][0])    #group(1)=A_1 group(2)=7
        if mbus:
            for h in mylist[i]:  #going horizonal(list within list)
                mbusValue=re.search(r'^b([x01]+)',h)
                if mbusValue:
                    if len(mbusValue.group(1))==1:
                        for k in range(len(mylist)):
                            mbusName=re.search(re.escape(mbus.group(1))+ r'\[(\d+)\]',mylist[k][0])
                            if mbusName:
                                mylist[k].append(mbusValue.group(1))
                    else:
                        partialList=list(mbusValue.group(1))
                        addZeros=int(mbus.group(2))+1-len(partialList)
                        for a in range(addZeros):
                            partialList.insert(0,'0')  #adding 0's to complete the full bus data
                        partialList.reverse()
                        for m in range(len(mylist)): #going vertically entire list
                            for j in range(len(partialList)): #bit index
                                mbusNameBit=re.search(re.escape(mbus.group(1))+ r'\['+str(j)+r'\]',mylist[m][0])
                                if mbusNameBit:
                                    mylist[m].append(partialList[j])         
                mtime=re.search(r'\d+[a-z]',h)
                if mtime:
                    for k in range(len(mylist)):
                        mbusName=re.search(re.escape(mbus.group(1))+ r'\[(\d+)\]',mylist[k][0])
                        if mbusName:
                            mylist[k].append(mtime.group())
    result=[]                        
    for i in range(len(mylist)):    #removing bus data from the list
        mbus=re.search(r'([^\[]+)\[(\d+):0\]',mylist[i][0])    
        if mbus:
            result.append(mylist[i])
    for i in result:
        mylist.remove(i)
                   
def makePwl(input):     #takes in captured signal list and outputs pwl format in a file
    finalContent=''
    for i in range(len(input)):
        content='vv1'
        input[i].insert(1,'0 dc 0 pwl (0')
        for j in range(len(input[i])):
            content = content + str(' ') + input[i][j]
        content = content + ')'
        finalContent = finalContent + content + '\n'
    print(finalContent)
    outputFile = open('vcd2pwl.out','w')
    #outputFile = open(sys.argv[2],'w')
    outputFile.write(finalContent)
    outputFile.close()

signalsDict=collectSignals()
print(signalsDict)
timescale=timescale()
printScreen()
mylist=captureData()
bus2bitConversion()
print(mylist)
makePwl(mylist)
