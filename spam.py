#Assumptions: a List Data structure has been used to contain the input dataset, intermediate and final results.
import re


# n_sequences = 4   #SID
# n_attributes = 2  #a,b,c,d,e,f
#
# v_dataset = []
#
# for i in range(n_attributes):
#     v_dataset.append([]) #item 0,1
#
# for i in range(n_sequences):
#     v_dataset[0].append([])
#     v_dataset[1].append([])
#
# v_dataset[0][0] = [0,1,2,3]
# v_dataset[0][1] = [0]
# v_dataset[0][2] = [0,1]
# v_dataset[0][3] = [0]
# v_dataset[1][0] = [1,3]
# v_dataset[1][1] = [0,1]
# v_dataset[1][2] = [0,2]
# v_dataset[1][3] = [1]


f = open("SIGN.txt","r")
data = f.read()
data = data.replace('\n',' ')
data = data.split(' ')

n_sequences = 1

dataset_length = len(data)

for i in range(dataset_length):
    item = data[i] = int(data[i])
    if item == -2:
        n_sequences+=1

n_attributes = max(data)

v_dataset2 = []
for i in range(n_attributes):
    v_dataset2.append([])
    for j in range(n_sequences):
        v_dataset2[i].append([])

current_pos = 0
current_seq = 0

for item in data:
    if int(item) == -1:
        current_pos += 1
    elif int(item) == -2:
        current_pos = 0
        current_seq += 1
    else:
        v_dataset2[int(item) - 1][current_seq].append(current_pos)


def getSupport(v_item):
    n = 0
    for i in range(n_sequences):
        if len(v_item[i]) > 0:
            n+=1
    return n

def s_extension(v_item1, v_item2):
    # Prepare result array
    result = []
    for customer_id in range (n_sequences):
        result.append([])

    for customer_id in range(n_sequences):
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
    for customer_id in range (n_sequences):
        result.append([])
    # Check for overlapping itemset indexes
    for customer_id in range (n_sequences):
        for entry1 in v_item1[customer_id]:
            for entry2 in v_item2[customer_id]:
                if entry1 == entry2:
                    result[customer_id].append(entry1)

    return result

def spam(dataset, minsup):
    print ("\nSPAM function call for:")
 #   print("Dataset:")
 #   print(dataset)
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
            frequent_items2 = frequent_items[i+1:] #copying by value;
        except ValueError:
            frequent_items2 = []
        pat = str(frequent_items[i]+1)+','+':'+str(frequent_items_support[i])
        result = search(dataset, dataset[frequent_items[i]], pat, frequent_items, frequent_items2, minsup, result)

    display_results(result)

    return result

# v_pat is defined vertically
def search(v_dataset, v_pat, pat, Sn, In, minsup, mined_sequences):
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
            Stemp2 = Stemp[i+1:] # copying by value
        except ValueError:
            Stemp2 = []

        search(v_dataset, s_extension(v_pat, v_dataset[Stemp[i]]),pat+'_'+str(Stemp[i]+1)+','+':'+str(Stemp_sup[i]), Stemp, Stemp2, minsup, mined_sequences)

    for item in In:
        support = getSupport(i_extension(v_pat, v_dataset[item]))
        if  support >= minsup:
            Itemp.append(item)
            Itemp_sup.append(support)
    for i in range(len(Itemp)):
        try:
            Itemp2 = Itemp[i+1:]
        except ValueError:
            Itemp2 = []
        search(v_dataset, i_extension(v_pat,v_dataset[item]),pat+str(Itemp[i]+1)+','+':'+str(Itemp_sup[i]), Itemp, Itemp2, minsup, mined_sequences)

    return mined_sequences

def display_results(mined_sequences):
    no_of_mined_sequences = len(mined_sequences)
    print('\nFound %d frequent sequential patterns:\n' % no_of_mined_sequences)

    for i in range(no_of_mined_sequences):
        mined_sequences[i] = mined_sequences[i].replace(',_','_')
        mined_sequences[i] = mined_sequences[i].split(':')

    mined_sequences = sorted(mined_sequences, key=lambda l:l[1], reverse=True) #comment this for sorting via item number

    for i in range(no_of_mined_sequences):
        raw_sequence = mined_sequences[i][0][:-1]
        support = int(mined_sequences[i][1])
        relative_support = support/n_sequences

        sequence = '{' + raw_sequence.replace('_','},{') + '}'

        print("%d:" % (i+1))
        print("Sequence: %s" % sequence)
        print("Absolute support: %d" % support)
        print("Relative support: %f\n " % relative_support)



# spam(v_dataset, 3)
spam(v_dataset2, 400)
