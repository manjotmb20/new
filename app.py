from flask import Flask,render_template,request
from elasticsearch import Elasticsearch


# paper_key=pickle.load(open("paper_key2.pickle","rb"))
# paper_title=pickle.load(open("paper_title.pickle","rb"))
# paper_abstract=pickle.load(open("paper_ab.pkl","rb"))

app = Flask(__name__)
es = Elasticsearch('localhost', port=9200)
a="e"

print("ye")
@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    # query_vec = model_emb([search_term])[0].numpy().tolist()

    res = es.search(
        index="base-index6", 
        size=20, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "cit_cont",
                        "paper_abs"
                    ] 
                }
            }
        }
    )
    # res=es.search(index="base-index3",
    #           size=50,
    #           body={
    #               "query": {
    #     "script_score": {
    #         "query": {"match_all": {}},
    #         "script": {
    #             "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
    #             "params": {"query_vector": query_vec}
    #         }
    #     }
    # }
    #           })
    # baseline=[]
    # name=dict()
    # abstract=[]
    # i=0
    name=set()
    key=dict()
    cont=dict()
    for hit in res['hits']['hits']:
    #     # tokenized_abstract = tokenizer.encode_plus(search_term+' '+hit['_source']['ABSTRACT'], max_length=320,pad_to_max_length=True,truncation=True,return_attention_mask=True,return_token_type_ids=False,return_tensors='pt')
    #     # tokenized_context = tokenizer.encode_plus(search_term+' '+hit['_source']['TITLE'], max_length=320,pad_to_max_length=True,truncation=True,return_attention_mask=True,return_token_type_ids=False,return_tensors='pt')
    #     # # print(search_term+' '+hit['_source']['TITLE'])
    #     # input_ids_abstract=tokenized_abstract['input_ids'].to(device)
    #     # att_mask_abstract=tokenized_abstract['attention_mask'].to(device)
    #     # input_ids_context=tokenized_context['input_ids'].to(device)
    #     # att_mask_context=tokenized_context['attention_mask'].to(device)
    #     # l=model(input_ids_abstract,att_mask_abstract,input_ids_context,att_mask_context)
    #     # logits = torch.sigmoid(l)
    #     # logits=logits.cpu()
    #     # logits = logits.detach().numpy()
    #     # logits=np.round(logits)
    #     # if(logits==1.0):
    #     #     baseline.append("Baseline")
    #     # else:
    #     #     baseline.append("Non-Baseline")  
    #     if(logits==1.0):
    #         if(hit['_source']['TITLE'] in paper_key.keys()):
    #             for key in paper_key[hit['_source']['TITLE']]:
    #                 try:
    #                     name[paper_title[key]]=[paper_abstract[key],"https://www.aclweb.org/anthology/"+key+"/"]
    #                 except:
    #                     print("not found")    
    #         else:
    #             continue
    #     # else:
    #     #     if(hit['_source']['TITLE'] in paper_key.keys()):
    #     #         name.append(paper_title[hit['_source']['TITLE']])
    #     #     else:    
    #     #         name.append("Not baseline: {} ".format(hit['_source']['TITLE']))

        

        name.add(hit['_source']['paper_name'])
        key[hit['_source']['paper_name']]=hit['_source']['key_paper']
        cont[hit['_source']['paper_name']]=hit['_source']['abstract']
    

    return render_template('results.html', res=res , name=name, key=key,cont=cont )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001)    