
n_customers = 4   #SID
n_attributes = 7  #a,b,c,d,e,f
max_transactions = 10 # number of entries in itemsets cell

v_dataset = []

for i in range(n_attributes):
    v_dataset.append([])
    for j in range(n_customers):
        v_dataset[i].append([(3*i + 2 * j) % max_transactions])


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
            frequent_items2 = frequent_items
            frequent_items2.remove(item)
        except ValueError:
            pass
        pat = [[item]]
        search(v_dataset[item], pat, frequent_items, frequent_items2, minsup, result)
    return result

# pat is defined vertically
def search(v_pat, pat, Sn, In, minsup, mined_sequences):
    mined_sequences.append(pat)
    Stemp = []
    Itemp = []
    for item in Sn:
        if getSupport(s_extension(v_pat, v_dataset[item])) >= minsup:
            Stemp.append(item)
    for item in Stemp:
        try:
            Stemp2 = Stemp
            Stemp2.remove(item)
        except ValueError:
            pass
        pat.append([item])
        search(s_extension(v_pat, v_dataset[item]),pat , Stemp, Stemp2, minsup, mined_sequences)

    for item in In:
        if getSupport(s_extension(v_pat, v_dataset[item])) >= minsup:
            Stemp.append(item)
    for item in Itemp:
        try:
            Itemp2 = Stemp
            Itemp2.remove(item)
        except ValueError:
            pass
        pat[-1].append(item)
        search(i_extension(v_pat,v_dataset[item]),pat, Itemp, Itemp2, minsup, mined_sequences)

    return mined_sequences

print(spam(v_dataset, 1))





