# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 15:08:41 2019

@author: Taz
"""
import random
from collections import Counter
from timeit import default_timer as timer
from statistics import mean


time_start = timer()
num_pop_sort = []

def Initial_population_initialization(data):
    #data is the original sequences
    population = []
    pop_sort = []
    #empty list to store the population according to the
    #size we want and make all pos "-"
    sequence = ["-"]*desiredSequenceSize
    
    for a in data:
        lengthSeq = len(a)
        #getting a num list from 1 to len
        numList = func_numlist()
        
        #randomize the number list
        func_permutated_num_Generator(numList)
        
        #cut the randomized num list accordingly
        numList = numList[:lengthSeq]
        
        #sort the numbers
        numList.sort()
        
        for b in range(0,lengthSeq):
            temp1 = numList[b]
            temp2 = a[b]
            #putting base char accordingto the numbers
            sequence[temp1-1] = temp2
            
        #adding final sequence to population
        population.append(''.join(sequence))
        pop_sort.append(numList)
        sequence = ["-"]*desiredSequenceSize
        
    num_pop_sort.extend(pop_sort)
    
    return population

def FitnessFunction(data):
    fitness = [0]*len(data)
    #----change----#
    #fitness fucntion vlaue calculation is still inprogress
    #must get a a valied scoring matrix in place for 
    #it to work smoothly
    #current one works almost as intended
    column = []
    value = 0
    
    for a in range(len(data[0])):
        column = [item[a] for item in data]
        if column[0] == "-":
            value -=1
        if column[0] != "-":
            value += Counter(column).most_common(1)[-1][-1] / len(column)
            
    #----change----#
    fitness.append(value)
    
    return sum(fitness)*100

def func_numlist():
    #just creats a number list 
    #from 1 to n
    # n being the desired sequence size
    numlist = []
    
    for a in range(1,desiredSequenceSize+1):
        numlist.append(a)
        
    return numlist

def func_permutated_num_Generator(numlist):
    #shuffels the numbers in random order
    random.shuffle(numlist)
    
    return numlist

def Parent_gen(data):
    '''
    from the original sequences creats two parents
    '''
    parents = [Initial_population_initialization(data),Initial_population_initialization(data)]
    
    return parents

def OperatorSinglePoint(data):
    '''
    Both Parents are cut from the same randomly chosen position
    and 1st part of a parent is added to 2nd part of another parent
    to make two mutated parents
    '''
    child1f = []
    child1e = []
    
    child2f = []
    child2e = []
    
    child1 = []
    child2 = []
    
    parent1 = data[0]
    parent2 = data[1]
    
    parent1num = num_pop_sort[:len(num_pop_sort)//2]
    parent2num = num_pop_sort[len(num_pop_sort)//2:]
    
    random_num = random.randint(randpos-1,randpos+1)
    
    for a in range(len(originalSequences)):
#the value of random is very sensitive as it very much decides how much
#data will get matched too large distance will cause too many
# "-" hence making the calculation unnesessaily large
        
        parent1_num_cut = parent1num[a][:random_num]
        parent2_num_cut = parent2num[a][:random_num]
        
        parent1_firstHalf = parent1[a][:parent1_num_cut[-1]]
        parent1_lastHalf = parent1[a][parent1_num_cut[-1]:]
        
        parent2_firstHalf = parent2[a][:parent2_num_cut[-1]]
        parent2_lastHalf = parent2[a][parent2_num_cut[-1]:]
        
        child1f.append(parent1_firstHalf)
        child1e.append(parent2_lastHalf)
        
        child2f.append(parent2_firstHalf)
        child2e.append(parent1_lastHalf)

    f1max = len(max(child1f, key=len))
    e1max = len(max(child1e, key=len))
    
    f2max = len(max(child2f, key=len))
    e2max = len(max(child2e, key=len))
    
    for a in range(len(child1f)):
        while len(child1f[a])<f1max:
            child1f[a] = child1f[a]+'-'
            
    for a in range(len(child1e)):
        while len(child1e[a])<e1max:
            child1e[a] = '-'+child1e[a]
            
    for a in range(len(child2f)):
        while len(child2f[a])<f2max:
            child2f[a] = child2f[a]+'-'
            
    for a in range(len(child2e)):
        while len(child2e[a])<e2max:
            child2e[a] = '-'+child2e[a]
            
    for a in range(len(originalSequences)):
        child1.append(child1f[a]+child1e[a])
        
    for a in range(len(originalSequences)):
        child2.append(child2f[a]+child2e[a])
        
#        print ("Parent 1:",parent1[a],">Cut>",child1f[a],"len :",len(child1f[a]))
#        print ("Parent 2:",parent2[a],">Cut>",child1e[a],"len :",len(child1e[a]))
#        print ("offspring :",childs[a],"len :",len(childs[a]))
        
    return child1,child2

def OperatorUniformBlockExchange(data):

    g1 = None
    g2 = None
    
    child1 = []
    child2 = []
    
    father = data[0]
    mother = data[1]
    
    child1 = father.copy()
    child2 = mother.copy()
    
    p1matchdcolpos = []
    p2matchdcolpos = []
    
    p1colmatchd = []
    p2colmatchd = []
    
    for a in range(len(father[0])):
        #taking column 1 by 1
        column1 = [item1[a] for  item1 in father]
        
        #allS is True when all value in the the column1 is same
        allS = all(x==column1[0] for x in column1)
        
        if allS and column1[0] != '-':
           #if there is a all same column we store the column pos and column data
            p1matchdcolpos.append(a)
            p1colmatchd.append(column1)
            
    for a in range(len(mother[0])):
        column2 = [item2[a] for item2 in mother]
        alls = all(y==column2[0] for y in column2)
        
        if alls and column2[0] != '-':
            p2matchdcolpos.append(a)
            p2colmatchd.append(column2)
            
    if len(p1matchdcolpos) > 1 and len(p2matchdcolpos) > 1:
        gg = random.sample(p1matchdcolpos,2)
        gg.sort()
#        print (gg)
        
        fc1 = p1colmatchd[p1matchdcolpos.index(gg[0])]
        fc2 = p1colmatchd[p1matchdcolpos.index(gg[1])]
        
        if fc1 in p2colmatchd and fc2 in p2colmatchd:
#            print (fc1,fc2)
            temp1 = p2colmatchd.index(fc1)
            g1 = p2matchdcolpos[temp1]
             
            temp2 = p2colmatchd.index(fc2)
            g2 = p2matchdcolpos[temp2]
#        print (p2colmatchd,g1,g2)
            
        if g1 != None and g2!= None:
            #child1
            child1.clear()
            child2.clear()
            for a in range(len(originalSequences)):
                child1.append(father[a][:gg[0]+1]+mother[a][g1+1:g2]+father[a][gg[1]:])
            #child2
            
            for a in range(len(originalSequences)):
                child2.append(mother[a][:g1+1]+father[a][gg[0]+1:gg[1]]+mother[a][g2:])
#    for n in child1:
#        print (n)
#    for n in child2:
#        print (n)
#    print (mother_cut1,mother_cut2)
    return child1,child2
        
    
def OperatorRecombineMatchColumn(data):
    
    father = data[0]
    mother = data[1]
#    print (len(father),len(mother))
    child = []
    
    colPosFather = []
    fatherSeqCharNo = []
    
    motherCuts = []
    fatherCuts =[]
    
    #getting the matched columns of father
    for a in range(len(father[0])):
        
        column = [item[a] for item in father]
        same = all(d==column[0] for d in column)
        
        if same and column[0] != '-':
            colPosFather.append(a)
    
    #getting a random cut pos from father column positions
    def random_cut_point():
        random_cut = random.choice(colPosFather)
        
        if random_cut == len(father[0])-1:
            random_cut_point()
        else:
            return random_cut
        
    #getting the random cut point of father
    if len(colPosFather)>1:    
        random_cut = random_cut_point()
        father_cut_pos = random_cut
        if father_cut_pos == None:
            father_cut_pos = random_cut_point()
#        print (len(colPosFather),father_cut_pos,len(father[0]))
        else:
        #cutting all the father sequences
            for a in range(len(father)):
#                print (father[a],father_cut_pos)
                temp = father[a][:father_cut_pos+1]
                fatherCuts.append(temp)
                temp = temp.replace("-","")
                fatherSeqCharNo.append(len(temp))
            
        #cutting all the mother seqences
            for j in range(len(mother)):
                
                char = 0
                pos = 0
                
                for k in range(len(mother[0])):
                    
                    pos +=1
                    if mother[j][k] != "-":
                        char+= 1

                    if char == fatherSeqCharNo[j]:
                        motherCuts.append(mother[j][pos:])
                        break
                    
            if len(motherCuts) == numOfSequences :    
#                print (len(motherCuts))
                lenMax = len(max(motherCuts, key=len))
    #            print ("lenmax",lenMax,len(motherCuts))
    #    adding the spaces in junction points
                for a in range(len(mother)):
#                    print (len(motherCuts[a]),lenMax)
#                if not lenMax == len(motherCuts[a]):
                    while len(motherCuts[a]) < lenMax :
                        motherCuts[a] = "-" + motherCuts[a]
                
                #adding father part with mother part to create offspring
                for a in range(len(father)):
            #        print (len(motherCuts[a]))
                    child.append(fatherCuts[a] + motherCuts[a])
        
    if len(child):
        return child
    else:
        if random.randint(0,1):
            return father
        else:
            return mother
        
def OperatorChnageSpace(data):
    '''
    a randomly choosen das is replaced with a ramdomly choosen
    base char 
    '''
    
    copi = data.copy()
    
    das_pos = []
    cha_pos = []
    
    for x in range(len(data)):
        cha = []
        das = []
        
        for a in range(len(data[x])):
            if data[x][a] == '-':
                #getting the pos of the dash in the sequence
                das.append(a)
            else:
                #getting the pos of the base char's
                cha.append(a)
                
        das_pos.append(das)
        cha_pos.append(cha)
        
    for a in range(lamda):
        #getting a random seq to work on
        choosenSequence =random.choice(data)
        g = data.index(choosenSequence)
        
        #choosing random das and base char position
        if len(das_pos[g]) and len(das_pos[g]):
            ran_das = random.choice(das_pos[g])
            ran_cha = random.choice(cha_pos[g])
            
            listyy = list(choosenSequence)
            
            #removing the dash and insert the dash at the char position
            listyy.pop(ran_das)
            listyy.insert(ran_cha,"-")
            temp = ''.join(listyy)
            data[g] = temp

    new_s = FitnessFunction(data)
    old_s = FitnessFunction(copi)
    
    if new_s > old_s :
        
        return data
    
    else:
    
        return copi
        
def OperatorChnageSpaceMod(data,num):
    '''
    a randomly choosen das is replaced with a ramdomly choosen
    base char 
    '''
    das_pos = []
    cha_pos = []
    
    for x in range(len(data)):
        cha = []
        das = []
        
        for a in range(len(data[x])):
            if data[x][a] == '-':
                #getting the pos of the dash in the sequence
                das.append(a)
            else:
                #getting the pos of the base char's
                cha.append(a)
                
        das_pos.append(das)
        cha_pos.append(cha)
        
    #getting a random seq to work on
    choosenSequence = data[num]
    g = data.index(choosenSequence)
    
    if len(das_pos[g])>0 and len(cha_pos[g])>0:
        #choosing random das and base char position
        ran_das = random.choice(das_pos[g])
        ran_cha = random.choice(cha_pos[g])
        listyy = list(choosenSequence)
        
        #removing the dash and insert the dash at the char position
        listyy.pop(ran_das)
        listyy.insert(ran_cha,"-")
        temp = ''.join(listyy)
        data[g] = temp
        
    return data

def OperatorDecreaseSearchSpace(data):
    '''
    if a column is found where all is dash
    then that column is removed
    '''
    dasColumnPos = []
    
    len_items = len(data[0])
    len_data = len(data)
    
    for a in range(len_items):
        column = [item[a] for item in data]
        allSame = all(x==column[0] for x in column)
        if allSame and column[0] == "-":
            #getting the column where all is dash"-"
            dasColumnPos.append(a)
            
    if dasColumnPos:
        randomdelchoice = random.choice(dasColumnPos)
        
        for a in range(len_data):
            #deleting the dash from all the sequences
            data[a] = data[a][:randomdelchoice]+data[a][randomdelchoice+1:]
            
    return data

def OperatorMergeSpaceBLock(data):
    ''''
    This operator gets all the spaces of a sequences 
    then chooses a random sequence based on the value of lamda
    from the choosen sequence it chooses 2 random das
    and brings them together
    '''
    copy = data.copy()
    
    main_score = FitnessFunction(copy)
    
    das_data = []
    
    for x in range(len(data)):
        das = []
        
        for a in range(len(data[x])):
            if data[x][a] == "-":
#                getting the position of all the dashs
                das.append(a)
                
        das_data.append(das)
        
    for a in range(lamda):
        
        choosenSequence = random.choice(data)
        seqIndex = data.index(choosenSequence)
        
        if len(das_data[seqIndex])>2:
            rand = random.sample(das_data[seqIndex],2)
            ran_das1 = rand[0]
            ran_das2 = rand[1]
            choosenSequencelisted = list(choosenSequence)
            choosenSequencelisted.pop(ran_das1)
            choosenSequencelisted.insert(ran_das2,"-")
            temp = "".join(choosenSequencelisted)
            data[seqIndex] = temp

    secd_score = FitnessFunction(data)
    
    if main_score > secd_score :
        
        return copy
    
    else:
        
        return data
    
def OperatorColumnAllDash(data):
    '''
    this column checks for a weak column like most of the data are spaces
    if such column is found then it moves a space so it can make the whole
    column spaces
    "-"      "-"
    "-"----> "-"
    "A"----> "-"
    "-"      "-"
    The A is moved to make a whole complete column full fo spaces
    ''' 
    possibleChangedPos = []
    weakcolpos = []
    weakcol = []
    for a in range(len(data[0])):
        #getting each column
        column = [item[a] for item in data]
        
        #checking which column has what the highest times
        gg = Counter(column).most_common(1)[-1]
        
        #selecting the column with most dash's
        if gg[0] == "-" and gg[1] == len(data)-1:
            weakcolpos.append(a)
            weakcol.append(column)
            
    #print ('weakcol',weakcol,'weakcolpos',weakcolpos)
    #pos of char to replace
    if len(weakcolpos):
        
        colToChange_posOfchar = random.choice(weakcolpos)
        temp = weakcolpos.index(colToChange_posOfchar)
        col = weakcol[temp]
        #print ('colToChange_posOfchar',colToChange_posOfchar,col)
        
        #selecting which seq has the char
        for a in range(len(col)):
        
            if col[a] != "-":
                seqToWorkOnNum = a
                selectedChar = col[a]
                
        sequenceToWorkOn = data[seqToWorkOnNum]  
              
        #print ('seq to work on>', seqToWorkOnNum+1  ,
        #       'pos of char>', colToChange_posOfchar,
        #       'change char>',selectedChar,
        #       )
        
        #getting the pos of dashs if thy exist next to cahr
        
        for a in range (colToChange_posOfchar,len(sequenceToWorkOn)):
            
            if sequenceToWorkOn[a] == '-':
                
                possibleChangedPos.append(a)
                
        for a in range(colToChange_posOfchar,0,-1):
            
            if sequenceToWorkOn[a] == '-':
                
                possibleChangedPos.append(a)
        
        #print ("Possible changed Position :",possibleChangedPos)
        if len(possibleChangedPos):
            randpos = possibleChangedPos[0]
            #print ("Selected position to change with:",randpos)
            work = list(sequenceToWorkOn)
            work.pop(colToChange_posOfchar)
            #print (work)
            work.insert(randpos,selectedChar)
            sequenceToWorkOn = "".join(work)
            data[seqToWorkOnNum] = sequenceToWorkOn
            
#    print ('cad',type(data))
    return data

def OperatorCatchMatchColumn(data):
    '''
    This operator checks of matched columns at first
    after finding all the matched column it chooses randomly
    a matched column then checks if the next base char of
    that coulumn in all the seq can be match by repositiong the 
    spaces
    '''
    
    copi = data.copy()
#    print (type(copi))
    sameCol = []
    col = []
    next_char = []
    next_char_pos = []
#    print ('cmc1')
    #getting all the same columns
    for a in range(len(data[0])):
        
        column = [item[a] for item in data]
        same = all(x==column[0] for x in column)
        if same:
            sameCol.append(a)
            col.append(column)
#    print ("Same pos columns :",sameCol)
            
            #randomly choosen column to work with
    if len(sameCol):
        rand_col = random.choice(sameCol)
#        print ('cmc2')
        
    #making sure it isnt the last column
        if rand_col != len(data[0])-1:

            #getting the next char of all the seq 
#            print ('cmc3')
            for x in range(len(data)):
                for a in range (rand_col,len(data[0])-1):
                    if (data[x][a+1]) != '-':
                        next_char.append(data[x][a+1])
                        next_char_pos.append(a+1)
                        break
            #checking if all the char r same?
            sameData = all(x==next_char[0] for x in next_char)
            #if same then put them in same column
            
            if sameData and len(next_char_pos) == len(data):
#                print ('cmc4')
                for a in range(len(data)):
                    
                    work = list(data[a])
                    work.pop(next_char_pos[a])
                    work.insert(next_char_pos[a],'-')
                    work.insert(rand_col+1,next_char[0])
                    temp = ''.join(work)
                    data[a] = temp
                    
            else:
#                print ('1',type(copi))
                return copi
            
#            print ('2',type(data))
            return data
        
        else:
#            print ('3',type(copi))
            return copi
    else:
        
        return copi
    
    
def OperatorCollectSpace(data):
    '''
    this operator collect spaces and puts them together
    '''
#    print ('cs',type(data))
    
    for x in range(lamda):
        sequence = random.choice(data)
        sequencenum = data.index(sequence)
        das_pos = []
        
        #getting all das pos of the randomly choosen sequence
        for a in range(len(sequence)):
            
            if sequence[a] == '-':
                
                das_pos.append(a)
        
        if len(das_pos)>2:
            
            rand_das = das_pos[int(len(das_pos)/2)]
            rand_das_pos = das_pos.index(rand_das)
            close2 = []
            close = []
            
            #getting the next close 3 spaces
            if bool(das_pos[rand_das_pos+1]) == True :
    
                close2.append(rand_das_pos+1)
                
            if bool(das_pos[rand_das_pos-1]) == True:
                
                close2.append(rand_das_pos-1)
                
            else:
                break
            
            for a in range(len(close2)):
                
                close.append(das_pos[close2[a]])
                
            work = list(sequence)
            
            #putting them all together by removing them from
            #their original position and then putting them next to 
            #randomly choosen das
            for index in sorted(close,reverse = True):
                del work[index]
                
            for a in range(len(close)):
                work.insert(rand_das,'-')
            temp = ''.join(work)
            
            data[sequencenum] = temp
        
    return data  
  
def OperatorMoveToHigherScore(data):

    copi = data.copy()
    
    for a in range(lamda):
        
        rand_sequence = random.choice(data)
#        print ("Sequence :",rand_sequence)
        rand_sequenceIndex = data.index(rand_sequence)
#        print ('seq No.:', rand_sequenceIndex+1)
        
        
        char_data = []
        
        #getting all the char's pos that has '-' close to it
        for a in range(len(rand_sequence)):
    
            if rand_sequence[a] != '-' :
                
                if a == 0 :
                    if rand_sequence[a+1] == '-' :
                        char_data.append(a)
                        
                elif a == len(rand_sequence)-1 :
                    if rand_sequence[a-1] == '-' :
                        char_data.append(a)
                        
                else:
                    if rand_sequence[a-1] == '-' or rand_sequence[a+1] == '-' :
                        char_data.append(a)
        
        #chooosing a random char from the list
        if len(char_data):
            rand_char = random.choice(char_data)
#        print ('char data:', rand_char,rand_sequence[rand_char])
            gg = rand_sequence[rand_char]
        
            #getting the dash's next to the randomed char
            
            dash_data = []
            
            for a in range (rand_char-1,0,-1):
                
                if rand_sequence[a] == '-':
                    dash_data.append(a)
                    
                else:
                    break
                
            for a in range (rand_char+1,len(rand_sequence)):
                
                if rand_sequence[a] == '-':
                    dash_data.append(a)
                    
                else:
                    break
                    
            dash_data.sort()
    #        print ('dash data :', dash_data)
            
            #move char to dash position's and get fitness value
            
            
            new_fitn = []
            new_seqs = []
            new_seqs.append(rand_sequence)
    
            for a in range(len(dash_data)):
                
                temp = list(rand_sequence)
                
    #            temp.pop(dash_data[a])
    #            temp.insert(rand_char,'-')
                
                temp.pop(rand_char)
                temp.insert(dash_data[a],gg)
                
                temp = ''.join(temp)
                new_seqs.append(temp)
            
            for a in range(len(new_seqs)) :
                
                temps = data
                temps[rand_sequenceIndex] = new_seqs[a]
                new_fitn.append(FitnessFunction(temps))
    #            print (temps,'=',new_fitn[a])
            
            #selecting the max fitness and getting the best seq
            maxFit = max(new_fitn)
            index = new_fitn.index(maxFit)
            
            bestSeq = data
            bestSeq[rand_sequenceIndex] = new_seqs[index]
    #        print (bestSeq)
    
            return bestSeq  
        
        else:
            
            return copi

def CroOperatorDecomposition(data):
    
#    print ("Decomposition")
    
    block = []
    column = []
    
    p1front = []
    p1end = []
    
    child1 = []
    child2 = []
    
    work = []
    
        
    for a in range(len(data[0])):
        
        temp = [item[a] for item in data]
        
        alsame = all(x==temp[0] for x in temp)

        if not alsame:
            
            column.append(a)
            
        if alsame:
            
            block.append(column)
            column = []
            
        if a == len(data[0])-1:
            
            block.append(column)
            column = []
        
    index = max((len(l), i) for i ,l in enumerate(block))[1]
    items = block[index]
        
    fc1,fc2 = items[0],items[-1]


    for a in range(len(data)):
        
        p1front.append(data[a][:fc1])
        p1end.append(data[a][fc2+1:])
        
        work.append(data[a][fc1:fc2+1])
        
#    print (work)
    child1 = OperatorChnageSpace(work)
    child2 = OperatorMoveToHigherScore(work)
    
#    print (child1)
#    print (child2)
    
    for a in range(len(data)):
        
        child1[a] = p1front[a] + child1[a] + p1end[a]
        
        child2[a] = p1front[a] + child2[a] + p1end[a]
    
    return child1,child2


def CroOperatorInnerMoleculerIneffectiveCollisions(data):
    
#    print ("InnerMoleCularblahlbah")
    
    father = data[0]
    mother = data[1]
    
    father_cut_pos = random.randint(1,len(father[0])-1)

    fatherCuts1 = []
    fatherCuts2 = []
    
    motherCuts1 = []
    motherCuts2 = []
    
    child1 = []
    child2 = []
    
    fatherSeqCharNo = []
    
    for a in range(len(father)):
        temp1 = father[a][:father_cut_pos]
        temp2 = father[a][father_cut_pos:]
        fatherCuts1.append(temp1)
        fatherCuts2.append(temp2)
        temp1 = temp1.replace("-","")
        fatherSeqCharNo.append(len(temp1))
        
    #cutting all the mother seqences
    for j in range(len(mother)):
        
        char = 0
        pos = 0
        
        for k in range(len(mother[0])):
            pos +=1
            if mother[j][k] != "-":
                char+= 1
                
            if char == fatherSeqCharNo[j]:
                motherCuts2.append(mother[j][pos:])
                motherCuts1.append(mother[j][:pos])
                break

    lenMax = len(max(motherCuts2, key=len))
#    print ("lenmax",lenMax)
#    adding the spaces in junction points
    
    for a in range(len(mother)):
        while len(motherCuts2[a]) <lenMax :
            motherCuts2[a] = "-" + motherCuts2[a]
            
    lenMaxx = len(max(motherCuts1, key=len))
    
    for a in range(len(father)):
        while len(motherCuts1[a]) < lenMaxx :
            motherCuts1[a] = motherCuts1[a] + "-"
    
    #adding father part with mother part to create offspring
    for a in range(len(father)):
#        print (len(motherCuts2[a]))
        child1.append(fatherCuts1[a] + motherCuts2[a])
        child2.append(motherCuts1[a] + fatherCuts2[a])
    

#    for a in range(4):
#        print('c1>',child1[a])
#    for a in range(4):
#        print('c2>',child2[a])
    return child1,child2

def func_CRO_fitness(data):
    
#    print ("CRO special fitness")
    
    def fit(lel):
        #function to get score
        
        score = None
        same = all(x==lel[0] for x in lel)
        
        if same:
            #if all same
            score = 1
#            print (lel,score)
            
        elif not same and not all(c in lel for c in '-'):
            #all differant and theres no '-'
            score = 0
#            print (lel,score)
            
        elif lel[1] == '-':
            #main is '-'
            if lel[0] == '-' and lel[2] != '-' or lel[0] != '-' and lel[2] == '-':
                #one is '-' and other char
                score = .7
#                print (lel,score)
            else:
                score = .4
#                print (lel,score)
                
        elif lel[1] != '-':
            # main is char
            if lel[0] == '-' and lel[2] != '-' or lel[0] != '-' and lel[2] == '-':
                #one is '-' and other is char
                if lel[1] == lel[2] or lel[1] == lel[0]:
                    score = .7
#                    print (lel,score)
                else:
                    score = .2
#                    print (lel,score)
            else:
                score = .4
#                print (lel,score)
            
        return score
        
        
    columns = []
    raw_all_score = []
    score_parts = []
    score = []
    
    #getting all columns
    for a in range(len(data[0])):
        column = [item[a] for item in data]
        columns.append(column)
    
    for col in range(len(columns)):

        for a in range(len(columns[col])):
            
            if a == 0:
                temp = columns[col][-1]+columns[col][a]+columns[col][a+1]
                
            elif a == len(columns[col])-1:
                temp = columns[col][a-1]+columns[col][a]+columns[col][0]
                
            else:
                temp = columns[col][a-1]+columns[col][a]+columns[col][a+1]
           
            raw_all_score.append(fit(temp))
    for i in range(0, len(raw_all_score), len(data)):
        parts = raw_all_score[i:i + len(data)]
        score_parts.append(parts)
        
    
    for a in range(len(score_parts[0])):
        c = [item[a] for item in score_parts]
        temp = sum(c)
        score.append('%.1f'%(temp))
    
#    print (score)
        
    
    index = score.index(min(score))
    
#    print (index)
    
    return index

def CroOperatorSynthesis(data):
    
#    print ("CRO sysnthesis")
    
    father = data[0]
    mother = data[1]
    
    child = []
    
    f_matchd_columns = []
    m_matchd_columns = []
    
    f_matchd_col_pos = []
    m_matchd_col_pos = []
    
    f_seq_char_no = []
    
    cut_father = []
    cut_mother = []
    
    for a in range(len(father[0])):
        
        col = [item[a] for item in father]
        allsame = all(x==col[0] for x in col)
        if allsame and col[0] != '-':
            f_matchd_columns.append(col)
            f_matchd_col_pos.append(a+1)
    
    for a in range(len(mother[0])):
        
        col = [item[a] for item in mother]
        allsame = all(x==col[0] for x in col)
        if allsame and col[0] != '-':
            m_matchd_columns.append(col)
            m_matchd_col_pos.append(a+1)
    
    if len(f_matchd_col_pos):
        for a in range(len(father)):
            
            temp = father[a][:f_matchd_col_pos[-1]]
            cut_father.append(temp)
            temp = temp.replace('-','')
            f_seq_char_no.append(len(temp))
            
        for a in range(len(mother)):
            
            char= 0
            pos = 0
            
            for k in range(len(mother[0])):
                
                pos += 1
                
                if mother[a][k] != '-' :
                    char += 1
                    
                if char == f_seq_char_no[a] :
                    cut_mother.append(mother[a][pos:])
                    break        
            
        lenMax = len(max(cut_mother , key=len))
        
        for a in range(len(cut_mother)):
            while len(cut_mother[a]) < lenMax :
                cut_mother[a] = '-' + cut_mother[a]
        
        for a in range(len(father)):
            
            child.append(cut_father[a]+cut_mother[a])
    
        return child
    
    else:
        
        if random.randint(0,1):
            
            return father
        
        else:
            
            return mother
    
##########################>?MAIN?<###################################
_file_name = "Sir_data/D15.txt"

input_file = open(_file_name,"r")
outputfile = open("run2/output(D15).txt","w+")

numOfSequences = sum(1 for line in open(_file_name))

originalSequences = []*numOfSequences
originallen = []
 
for a in range(0,numOfSequences):
    
    temp = input_file.readline()
    originalSequences.append(temp.rstrip("\n"))
    originallen.append(len(temp.rstrip("\n")))
    
#print (originallen)
maxlen = max(originallen)
#print (maxlen)

meanlen = mean(originallen)
#print (meanlen)

randpos = int(maxlen/2)

scaling_factor = 1.00
desiredSequenceSize = int(scaling_factor*maxlen)
print ('maxlen',maxlen,'minlen',min(originallen),'no of s',len(originalSequences))

lamda = int(.3*len(originalSequences))

##############################

fitness = []
sequences = []


#----------checking data-----------#

iteration = 10000

CRO_count = 0
CRO_limit = 400000

outputfile.write('Data set : %s\nIteration : %d\nCRO_count : %d\n' % (_file_name,iteration,CRO_limit))


for a in range(iteration):
    
    print ("Iter :",a+1)
    
    if CRO_count == CRO_limit:
        
        break
    
    '''GA Start'''
    #Sexual reproduction
    parents = Parent_gen(originalSequences)
    parents = OperatorSinglePoint(parents)
#    parents = OperatorUniformBlockExchange(parents)
    
    #Mutation
    offspiring = OperatorRecombineMatchColumn(parents)
    offspiring = OperatorChnageSpace(offspiring)
    offspiring = OperatorDecreaseSearchSpace(offspiring)
    offspiring = OperatorMergeSpaceBLock(offspiring)
    offspiring = OperatorColumnAllDash(offspiring)
    offspiring = OperatorCatchMatchColumn(offspiring)
    offspiring = OperatorCollectSpace(offspiring)
    offspiring = OperatorMoveToHigherScore(offspiring)
#    print ('%.1f'%(FitnessFunction(offspiring)))
    '''GA End'''
    
    _pe = FitnessFunction(offspiring)
    _ke = random.uniform(0,1)
    piu = random.uniform(_ke,1)
    
    '''CRO Start'''
    x = func_CRO_fitness(offspiring)
    offspiring = OperatorChnageSpaceMod(offspiring,x)
    
    CRO_count += 1
    pe = FitnessFunction(offspiring)
    ke = ( _pe + _ke - pe)*piu
    
    parents = CroOperatorDecomposition(offspiring)
    
    CRO_count += 1
    pe = FitnessFunction(offspiring)
    ke = ( _pe + _ke - pe)*piu
    
    parents = CroOperatorInnerMoleculerIneffectiveCollisions(parents)
    
    CRO_count += 1
    pe = FitnessFunction(offspiring)
    ke = ( _pe + _ke - pe)*piu
    
    offspiring = CroOperatorSynthesis(parents)   
    
    CRO_count += 1
    pe = FitnessFunction(offspiring)
    ke = ( _pe + _ke - pe)*piu
    
    '''CRO End'''
    
    fitness.append('%.1f'%(FitnessFunction(offspiring)))
    sequences.append(offspiring)
    
    '''writing on file'''
#    outputfile.write('\nIteration  %d : ' % (a+1))
#    outputfile.write('%.1f'%(FitnessFunction(offspiring)))
    '''writing on file'''


get_max_fit = max(fitness)
index = fitness.index(get_max_fit)
max_fit_seq = sequences[index]

m_s = 0

for o in range(len(max_fit_seq[0])):
    
    col = [item[o] for item in max_fit_seq]
    
    match = all(x==col[0] for x in col)
    
    if match:
        
        m_s += 1
        
result = m_s/maxlen

print (len(max_fit_seq[0]),m_s,'%.4f'%result)

outputfile.write('\n\nResult : %s' % ('%.4f'%result))

elapsed_time = timer() - time_start
outputfile.write("\nTime Taken to execute %d iteration : %d" % (iteration,elapsed_time))
#-------data checking------------#
input_file.close()
outputfile.close()