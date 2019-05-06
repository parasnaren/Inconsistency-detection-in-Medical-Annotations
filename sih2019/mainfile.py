import pandas as pd
from gensim.models import Word2Vec
import pickle

def assign_to_groups(entity):
    """
    create group names and assign entities to 
    their most similar group
    """
    print('Assigning entities to semantic groups.')
    #model = Word2Vec.load('word2vec.model')
    model = Word2Vec.load('word2vec_1.model')
    model.init_sims
    vocab = list(model.wv.vocab)
    groups = {}
    for key, val in entity.items():
    #for key, val in entity.items():
        if key in vocab:
            similar = model.wv.most_similar(key)[:3]  # load most similar words
            #print('Searching embedding.')
            most_similar = similar[0][0]
            flag = 0
            for term in similar:    # check in top 3 terms
                if term[0] in groups:  # check if the similar term exists
                    flag = 1
                    #print(term[0], ' -> ', key)
                    groups[term[0]].append(key)
                    break
            if not flag:
                #print(most_similar, ' -> ', key)
                groups[most_similar] = [key]
                            
        else:       # query not in vocabulary
            if key not in groups:
                #print(key, ' -> ', key)
                groups[key] = [key]
    
    #print(groups)
    
    with open('group.pickle', 'wb') as handle:
        pickle.dump(groups, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        
def get_consistency_tag(entities):
    cons = {}
    for key, val in entities.items():
        if len(val) > 1:
            max_val = 0
            for k, v in val.items():
                if v > max_val:
                    max_val = v
            for k, v in val.items():
                cons[key] = {k: 0}
                if v == max_val:
                    cons[key] = {k: 1}
    return cons
            
def create_output_dataset(entities, groups, cons, sentid):
    c = 0
    outfile = open('TeamCoders6_RG1_Evaluation.tsv', 'w')
    ourfile = open('for_ui.csv', 'w')
    for key, value in groups.items():
        outfile.write(key + '\t')
        for name in value:
            for tag, cnt in entities[name].items():
                sent = sentid[tag]
                tmp = tag + '_SentList_' + str(sent)
                outfile.write(tmp + '\t')
                ourfile.write(str(sent) + '\t' + key + '\t' + tag + '\t')
                #tmp = tag + '_' + str(sent)
                if name not in cons or tag not in cons[name]:
                    c = 1
                else:
                    c = cons[name][tag]
                    
                ourfile.write(str(c) + '\t')
        outfile.write('\n')
        ourfile.write('\n')
        
    outfile.close()
    ourfile.close()
    
#create_output_dataset(entities, groups, cons, entities_with_sentid)

def generate_majority_dict(path):
    """
    return all the tags and counts
    """
    infile = pd.read_csv(path)

    majority = {}
    for i, row in infile.iterrows():
        j = 2
        while row[str(j)] != '\n':
            if row[str(j)] in majority:
                majority[row[str(j)]] += 1
            else:
                majority[row[str(j)]] = 1
                
            j+=1
    majority_df = pd.DataFrame.from_dict(majority, orient='index')
    majority_df.to_csv('majority_file.csv')
    majority = pd.read_csv('majority_file.csv')
    majority.columns = ['words','counts']
    print('Tags-counts created.')
    return majority


def load_entity_sets(m):
    """
    load the multi word entities and their 
    different annotations
    """
    entity = {}
    for i in range(len(m)):
        tag, count = m.at[i, 'words'], m.at[i, 'counts']
        text = tag.split('$')
        query = ""
        for k in range(len(text)):
            if k%2 == 0:
                query += text[k] + ' '
        
        query = query.replace(' ', '_').rstrip('_')
        
        if query in entity:
            if tag in entity[query]:
                continue
            else:            
                entity[query][tag] = count
        else:
            entity[query] = {tag: count}
            
    print('Entity sets loaded.')
    return entity

def get_sentence_ids(path):
    """
    get list of sentence ids for each
    tagged annotation terms/relationships
    """
    
    entity_to_sentid = {}
    df = pd.read_csv(path)
    for i in range(len(df)):
        j = 2
        term = df.at[i, str(j)]
        #print(term)
        while term != '\n':
            if term in entity_to_sentid:
                entity_to_sentid[term].append(df.at[i, '0'])
            else:
                entity_to_sentid[term] = [df.at[i, '0']]
                
            j+=1
            term = df.at[i, str(j)]
        
    print('Sentence ids generated.')
    return entity_to_sentid

                
def mainfile():
    """
    run this file
    """
    
    df = []
    with open('AnnotatedData.tsv', 'r', encoding='utf8') as infile:
        for row in infile:
            text = row.split('\t')
            df.append(text)
        df = pd.DataFrame(df)

    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df[df[2] != '\n'].reset_index(drop=True)
    df = df.apply(lambda x: x.replace('none',''))
    df.to_csv('annotated_lower_removed.csv', index=False)
    path = 'annotated_lower_removed.csv'
    majority = generate_majority_dict(path)
    entities = load_entity_sets(majority)
    sentid = get_sentence_ids(path)
    
    # Comment if group.pickle is present
    # assign_to_groups(entities)
    
    groups = pickle.load(open('group.pickle', 'rb'))
    cons = get_consistency_tag(entities)
    create_output_dataset(entities, groups, cons, sentid)
    print('Output files created.')

if __name__ == "__main__":
    mainfile()
