def judge_new_chain(chain, tup):
    inchain = 0
    #print("chain: ",chain,"tup: ",tup)
    for i in range(len(chain)):
        if tup[i] == -1:
            continue
        if chain[i] == tup[i]:
            inchain += 1

    return inchain

def get_new_chain(chain,tup):
    newchain = []
    for i in range(len(chain)):
        if chain[i] == -1:
            newchain.append(tup[i])
        else:
            newchain.append(chain[i])
    return newchain

def add_tuple(chains, tups):
    ini_chains = []
    remove_chains = []
    append_chains = []
    for chain in chains:
        ini_chains.append(chain)
    for tup in tups:
        add = True
        for chain in ini_chains:
            inchain = judge_new_chain(chain,tup)
            if inchain == 1:
                if chain not in remove_chains:
                    remove_chains.append(chain)
                append_chains.append(get_new_chain(chain,tup))
                add = False
            elif inchain == 2:
                add = False
        if add:
            append_chains.append(tup)
    for chain in remove_chains:
        chains.remove(chain)
    for chain in append_chains:
        chains.append(chain)    
    return chains

#rel_plain_defen,rel_defenev_ap,rel_ap_ar,rel_plainev_ar
def find_chain(pair1,pair2,pair3,pair4,pair5,pair6):
    chains = []
    chains = add_tuple(chains,pair1)
    chains = add_tuple(chains,pair2)
    chains = add_tuple(chains,pair3)
    chains = add_tuple(chains,pair4)
    chains = add_tuple(chains,pair5)
    chains = add_tuple(chains,pair6)

    for chain in chains:
        if chain[0] == -1 and chain[1] != -1 and chain[2] == -1 and chain[3] != -1:
            chains.remove(chain)
        if chain[0] != -1 and chain[1] == -1 and chain[2] != -1 and chain[3] == -1:
            chains.append(chain)
    return chains
  

rel_plain_defen = []
rel_defenev_ap = [[1,1],[1,2],[2,1]]
rel_ap_ar = []
rel_plainev_ar = []
rel_plainev_ap = [[1,1],[1,2],[3,1]]
rel_defenev_ar = [[1,1],[1,3],[2,1]]
tups1 = []
tups2 = []
tups3 = []
tups4 = []
tups5 = []
tups6 = []

for p in rel_plain_defen:
    tups1.append([p[0],p[1],-1,-1])
for p in rel_defenev_ap:
    tups2.append([-1,p[0],p[1],-1])
for p in rel_ap_ar:
    tups3.append([-1,-1,p[0],p[1]])
for p in rel_plainev_ar:
    tups4.append([p[0],-1,-1,p[1]])
for p in rel_plainev_ap:
    tups5.append([p[0],-1,p[1],-1])
for p in rel_defenev_ar:
    tups6.append([-1,p[0],-1,p[1]])

chains = find_chain(tups1,tups2,tups3,tups4,tups5,tups6)
