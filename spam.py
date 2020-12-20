#Assumptions: a List Data structure has been used to contain the input dataset, intermediate and final results.


import re
import numpy as np
v_dataset = []

# PREPROCESSING DATASET

f = open("BIBLE.txt","r")
data = f.read()
test = re.split(' |\n', data)
test.pop(len(test)-1) # it removes the very last blank space, needed just to correctly process the values

row_element = []
row = []

# The list will contain itemsets for each different sequences that is ended by "-2", with "-1" we determine
# the end of an itemset
for elem in test:    
    if(int(elem) != -2 and int(elem) != -1):
        row_element.append(int(elem))
        row.append(row_element)             #  every row is composed by several itemsets (that are list as well)
        row_element = []                    # row is then made by row_element, every row_element is an itemset
    elif(int(elem) == -2):
       v_dataset.append(row)
       row = []

print(v_dataset[1])

#n_customers = 4   #SID
#n_attributes = 2  #a,b,c,d,e,f
#max_transactions = 5 # number of entries in itemsets cell

#for i in range(n_customers):
   # v_dataset[0].append([])
    #v_dataset[1].append([])

#v_dataset[0][0] = [0,1,2,3]
#v_dataset[0][1] = [0]
#v_dataset[0][2] = [0,1]
#v_dataset[0][3] = [0]
#v_dataset[1][0] = [1,3]
#v_dataset[1][1] = [0,1]
#v_dataset[1][2] = [0,2]
#v_dataset[1][3] = [1]


def getSupport(v_item):
    n = 0
    for i in range(n_customers):
        if len(v_item[i]) > 0:
            n+=1
    return n

def s_extension(v_item1, v_item2):
    # Prepare result array
    result = []
    for customer_id in range (n_customers):
        result.append([])

    for customer_id in range(n_customers):
        # Check if item1 appears for given customer:
        if len(v_item1[customer_id]) == 0:
            continue
        # Get a minimal itemset index for given customer for item1
        id1 = v_item1[customer_id][0]
        # Check for any itemset index for given customer for item2 greater than id1
        for entry in v_item2[customer_id]:
            if entry > id1:
                result[customer_id].append(entry)


    return result

def i_extension(v_item1, v_item2):
    # Prepare result array
    result = []
    for customer_id in range (n_customers):
        result.append([])
    # Check for overlapping itemset indexes
    for customer_id in range (n_customers):
        for entry1 in v_item1[customer_id]:
            for entry2 in v_item2[customer_id]:
                if entry1 == entry2:
                    result[customer_id].append(entry1)

    return result

def spam(dataset, minsup):
    print ("\nSPAM function call for:")
    print("Dataset:")
    print(dataset)
    print("Minsup:")
    print(minsup)
    frequent_items = []
    frequent_items_support = []

    result = []
    for item_id in range(n_attributes):
        support = getSupport(dataset[item_id])
        if  support >= minsup:
            frequent_items.append(item_id)
            frequent_items_support.append(support)
    for i in range(len(frequent_items)):
        try:
            frequent_items2 = frequent_items[:] #copying by value;
            frequent_items2.remove(frequent_items[i])
        except ValueError:
            pass
        pat = str(frequent_items[i])+','+':'+str(frequent_items_support[i])
        result = search(dataset[frequent_items[i]], pat, frequent_items, frequent_items2, minsup, result)

    display_results(result)

    return result

# v_pat is defined vertically
def search(v_pat, pat, Sn, In, minsup, mined_sequences):
    mined_sequences.append(pat)
    pat = pat.split(":")[0]
    Stemp = []
    Stemp_sup = []
    Itemp = []
    Itemp_sup = []

    for item in Sn:
        support = getSupport(s_extension(v_pat, v_dataset[item]))
        if support >= minsup:
            Stemp.append(item)
            Stemp_sup.append(support)
    for i in range(len(Stemp)):
        try:
            Stemp2 = Stemp[:] # copying by value
            Stemp2.remove(Stemp[i])
        except ValueError:
            pass

        search(s_extension(v_pat, v_dataset[Stemp[i]]),pat+'_'+str(Stemp[i])+','+':'+str(Stemp_sup[i]), Stemp, Stemp2, minsup, mined_sequences)

    for item in In:
        support = getSupport(i_extension(v_pat, v_dataset[item]))
        if  support >= minsup:
            Itemp.append(item)
            Itemp_sup.append(support)
    for i in range(len(Itemp)):
        try:
            Itemp2 = Itemp[:]
            Itemp2.remove(Itemp[i])
        except ValueError:
            pass
        search(i_extension(v_pat,v_dataset[item]),pat+str(item)+','+':'+str(Itemp_sup[i]), Itemp, Itemp2, minsup, mined_sequences)

    return mined_sequences

def display_results(mined_sequences):
    no_of_mined_sequences = len(mined_sequences)
    print('\nFound %d frequent sequential patterns:\n' % no_of_mined_sequences)

    for i in range(no_of_mined_sequences):
        mined_sequences[i] = mined_sequences[i].replace(',_','_')
        mined_sequences[i] = mined_sequences[i].split(':')
        raw_sequence = mined_sequences[i][0][:-1]
        support = int(mined_sequences[i][1])
        relative_support = support/n_customers

        sequence = '{' + raw_sequence.replace('_','},{') + '}'

        print("%d:" % (i+1))
        print("Sequence: %s" % sequence)
        print("Absolute support: %d" % support)
        print("Relative support: %f\n " % relative_support)



spam(v_dataset, 3)
