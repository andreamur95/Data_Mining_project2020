
n_customers = 4   #SID
n_attributes = 2  #a,b,c,d,e,f
max_transactions = 5 # number of entries in itemsets cell

v_dataset = []



v_dataset.append([]) #item 0
v_dataset.append([]) #item 1

for i in range(n_customers):
    v_dataset[0].append([])
    v_dataset[1].append([])

v_dataset[0][0] = [0,1,2,3]
v_dataset[0][1] = [0]
v_dataset[0][2] = [0,1]
v_dataset[0][3] = [0]
v_dataset[1][0] = [1,3]
v_dataset[1][1] = [0,1]
v_dataset[1][2] = [0,2]
v_dataset[1][3] = [1]

print(v_dataset)


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
    frequent_items = []
    result = []
    for item_id in range(n_attributes):
        if getSupport(dataset[item_id]) >= minsup:
            frequent_items.append(item_id)
    for item in frequent_items:
        try:
            frequent_items2 = frequent_items[:] #copying by value;
            frequent_items2.remove(item)
        except ValueError:
            pass
        pat = str(item)
        result = search(dataset[item], pat, frequent_items, frequent_items2, minsup, result)
    return result

# v_pat is defined vertically
def search(v_pat, pat, Sn, In, minsup, mined_sequences):
    mined_sequences.append(pat)
    Stemp = []
    Itemp = []
    for item in Sn:
        if getSupport(s_extension(v_pat, v_dataset[item])) >= minsup:
            Stemp.append(item)
    for item in Stemp:
        try:
            Stemp2 = Stemp[:] # copying by value
            Stemp2.remove(item)
            print("s",item, Stemp, Stemp2)
        except ValueError:
            pass
        pat += "_"
        pat += str(item)
        search(s_extension(v_pat, v_dataset[item]),pat , Stemp, Stemp2, minsup, mined_sequences)

    for item in In:
        if getSupport(i_extension(v_pat, v_dataset[item])) >= minsup:
            Itemp.append(item)
    for item in Itemp:
        print(Itemp)
        try:
            Itemp2 = Itemp[:]
            Itemp2.remove(item)
            print("i",item,Itemp,Itemp2)
        except ValueError:
            pass
        pat += str(item)
        search(i_extension(v_pat,v_dataset[item]),pat, Itemp, Itemp2, minsup, mined_sequences)

    return mined_sequences

print(spam(v_dataset, 3))

print(s_extension(s_extension(v_dataset[0],v_dataset[1]),v_dataset[1]))

