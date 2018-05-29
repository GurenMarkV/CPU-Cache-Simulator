#//////////////////////////////////////////////////////////////
#   DAKSH PATEL                                               #
#   104030031                                                 #
#   104030031_Assign5.py                                      #
#   Simulate Cache                                            #
#//////////////////////////////////////////////////////////////

import math

#Plenty of arrays to hold values and grab bits from
RW_Indicator= []
validBits   = []
dirtyBits   = []
rowBits     = []
dataArray   = []
WBArray     = []
LRU         = []
tempVar     = []
#Global Variables for some specific calculations and initializing to zero
blockSize   = 64
tag         = 24
row         = 6
block       = 0
ofst        = 2
hits        = 0
misses      = 0
cycles      = 0          
WB          = 0
associativity = 1       #Select 1,2,4,8,16

#init to zero
def initToZero():
    for x in range(0, blockSize):
        validBits.append(0)
        dirtyBits.append(0)
        LRU.insert(x, [])
        dataArray.insert(x, [])
        WBArray.insert(x, [])
        for y in range(0, associativity):
            LRU[x].append([])
            dataArray[x].append([])
            WBArray[x].append([])
            y = y
                                                 


# Open one file at a time and run sim

quickFile = open('quick/quick4k.txt', 'r')
# quickFile = open('quick/quick16k.txt', 'r')
# quickFile = open('quick/quick256k.txt', 'r')
# quickFile = open('quick/quick64k.txt', 'r')
# quickFile = open('quick-big/quick1M.txt', 'r')
# quickFile = open('random/random4k.txt', 'r')
# quickFile = open('random/random16k.txt', 'r')
# quickFile = open('random/random256k.txt', 'r')
# quickFile = open('random/random64k.txt', 'r')
# quickFile = open('random-big/random1M.txt', 'r')


initToZero() #Initialize values to zero, call function
for value in quickFile.readlines() :                                                                          
    RW_Indicator = value[:2]    #Specify the Read or Write letter location                                                                        
    valueInt = int(value[2:])   #Specify non RW letters and only numbers                                                                 
    data = f'{valueInt:032b}'   #Format numbers to binary data                                                              
    tagBit = data[0:24]
    rowBit = data[24:30]
    #block not used otherwise it would be here in order
    ofstBit = data[30:32]                          
    location = int(rowBit, 2) 
    
    if('R' in RW_Indicator):    #Read
        hits += 1                                                                           
        if(data[0] in dataArray):                                                           
            cycles += 1 + int(rowBit, 2)/2 + math.log2(associativity) 
            if(associativity == 1):
                pass                                                                        
            else:                                                                          
                col = LRU[int(rowBit, 2)].index(tagBit)                                 
                tempVar = ([LRU[int(rowBit, 2)][col]])
                LRU[location][0].insert(0, tempVar)                                       
                LRU[location][0].pop(associativity)                                      
                #Cache  - Dirtybit changes, line allocation/writing/evicting
                dirtyBits[int(rowBit, 2)] = 0
                validBits[int(rowBit, 2)] = 1
                col = dataArray[int(rowBit, 2)].index(data)  
                dirtyBits[int(rowBit, 2)] = 1
                dataArray[int(rowBit, 2)].insert(0, dataArray[int(rowBit, 2)])
                dirtyBits[int(rowBit, 2)] = 0
                validBits[int(rowBit, 2)] = 0
                dataArray[int(rowBit, 2)].pop(col)
    else:
        misses += 1
        cycles += 20 + 2**block
        validBits[int(rowBit, 2)] = 1 
        dirtyBits[int(rowBit, 2)] = 0
        if(associativity == 1):
            dataArray[location][0] = data
            LRU[int(rowBit, 2)][0] =  tagBit 
            # WB += 1                                      
        else:
            dirtyBits[int(rowBit, 2)] = 0
            LRU[location].insert(0, tagBit)
            LRU[int(rowBit, 2)].pop()  
            dirtyBits[int(rowBit, 2)] = 1                             
            WBArray[location][associativity-1] = dataArray[location][associativity-1] # copy to writeback array before overwriting cache location
            # WB += 1
            dataArray[location].insert(0, data)                                   
            dataArray[int(rowBit, 2)].pop()    
            dirtyBits[int(rowBit, 2)] = 0
            validBits[int(rowBit, 2)] = 0

    if('W' in RW_Indicator):        #Write
        if(data in dataArray):
            cycles += 1 + int(rowBit, 2)/2 + math.log2(associativity)          
            if(associativity == 1):
                pass                                                                        
            else:                                                                            
                col = LRU[int(rowBit, 2)].index(tagBit)                                 
                tempVar = ([LRU[int(rowBit, 2)][col]])
                hits += 1 + int(rowBit, 2)/2 + math.log2(associativity)    #Hits counter
                LRU[location][0].insert(0, tempVar)                                       
                LRU[location][0].pop(associativity)                                       
                #Cache - Dirtybit changes, line allocation/writing/evicting
                dirtyBits[int(rowBit, 2)] = 0
                validBits[int(rowBit, 2)] = 1
                col = dataArray[int(rowBit, 2)].index(data)  
                dirtyBits[int(rowBit, 2)] = 1
                dataArray[int(rowBit, 2)].insert(0, dataArray[int(rowBit, 2)])
                dirtyBits[int(rowBit, 2)] = 0
                validBits[int(rowBit, 2)] = 0
                dataArray[int(rowBit, 2)].pop(col)           
        else:
            cycles += 1 + 2**block
            validBits[int(rowBit, 2)] = 1 
            dirtyBits[int(rowBit, 2)] = 0
            if(associativity == 1):
                dataArray[location][0] = data 
                LRU[int(rowBit, 2)][0] =  tagBit  
                WB += 1                                     
            else:
                LRU[location].insert(0, tagBit)
                LRU[int(rowBit, 2)].pop()
                dirtyBits[int(rowBit, 2)] = 1                                       
                WBArray[location][associativity-1] = dataArray[location][associativity-1] # copy to writeback array before overwriting cache location
                WB += 1 #increment writebacks 
                dataArray[location].insert(0, data)                                   
                dataArray[int(rowBit, 2)].pop()   
                validBits[int(rowBit, 2)] = 0
                dirtyBits[int(rowBit, 2)] = 0    


print('Valid Bit Array:', validBits)
print('Dirty Bit Array:', dirtyBits)
print('Write Back Array:', WBArray)
print ('LRU Array:', LRU)
print('Data Array: ', dataArray )
print( 'Tagbits: ', len(tagBit), ', rowBits: ', row, ', Blockbits: ,', block, ', Associativity Level: ', associativity)
print('Total Cycles: ', cycles, ', SRAM Size:', associativity*2**6*58)
print('Hits:', hits, ', Misses: ', misses, ', Write Back Cost: ', WB)
    
quickFile.close()