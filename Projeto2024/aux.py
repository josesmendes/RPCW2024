import requests, json, re
from SPARQLWrapper import SPARQLWrapper, JSON


graphdb_endpoint = "http://localhost:7200/repositories/elden_ring"
def sparql_query_maker(query):
    sparql =SPARQLWrapper("http://localhost:7200/repositories/elden_ring/statements")
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def turn_to_json(dados, lista):
    for tipo in lista:
        linha = dados[0][tipo]["value"].replace("'", '"')
        dados[0][tipo]["value"] = json.loads(linha)
    return dados

def boss_list(dados):
    lista = []
    if "boss" in dados[0].keys():
        for entry in dados:
            lista.append((entry["boss"]["value"].split('/')[-1],entry["boss_name"]["value"]))
        dados[0]["boss"]["value"] = lista
    return dados    

def concat_eq(dados):
    runes = []
    drops = {}
    for entry in dados:
        rune = entry["runes"]["value"].replace("'", '"')
        if "drops" in entry.keys():
            drop = entry["drops"]["value"].split("/")[-1]
            if drop not in drops.keys():
                if "uper" in entry.keys():
                    link = f"{entry['uper']['value'].split('/')[-1].lower()}/{entry['type']['value'].split('/')[-1]}/{drop}"
                    drops[drop] = [link,entry["drop_name"]["value"]]
                else:
                    link = f"{entry['type']['value'].split('/')[-1].lower()}/{drop}"
                    drops[drop] = [link,entry["drop_name"]["value"]]
        if rune not in runes and "k" not in rune:
            runes.append(rune)
    runes.sort()
    dados[0]["runes"]["value"] = runes
    if "drops" in entry.keys():
        dados[0]["drops"]["value"] = drops
    return dados[0]

def limpa_tipos(dados):
    filter = ["isInRegion", "isInLocation", "Drops"]
    dadosp = []
    dadosn = []
    listaf = []
    dadossub = []
    for entry in dados:
        p = entry["p"]["value"].split('/')[-1]
        if p in filter:
            listaf.append(p)
        elif "rdf" not in p and p not in dadosp:
            dadosp.append(p)
        if "n" in entry.keys():
            n = entry["n"]["value"].split('/')[-1]
            if "rdf" not in n and n not in dadosn :
                dadosn.append(n)
        if "sub" in entry.keys():
            sub = entry["sub"]["value"].split('/')[-1]
            if sub not in dadossub:
                dadossub.append(sub)
    new_dados = {"p": dadosp}
    if dadosn:
        new_dados["n"] = dadosn
    if dadossub:
        new_dados["sub"] = dadossub
    if listaf:
        new_dados["prop"] = listaf
    return new_dados 

def get_values(lista, val_type):
    dicionario = {}
    for tipo in lista:
        if val_type == "n":
            sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name where {{
    ?s  :{tipo} ?o;
        :name ?name
}}
'''
        if val_type == "p":
            sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name where {{
    ?o  :{tipo} ?s.
    ?s  :name ?name
}}
'''
        resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
        if resposta.status_code == 200:
            dados = resposta.json()['results']['bindings']
            lista = []
            for entry in dados:
                val = entry["s"]["value"].split('/')[-1]
                nome = entry["name"]["value"].split('/')[-1]
                lista.append((val,nome))
            string = tipo + "_" + val_type
            dicionario[string] = lista
    return dicionario

def cria_dic(valor, chave):
    req_type = chave.split("_")[-1]
    if not valor:
        valor = 0
    return {"name":req_type, "amount":valor}

def cria_dic_scal(valor, chave):
    req_type = chave.split("_")[-1]
    if not valor:
        return None
    return {"name":req_type, "scaling":valor}

def insert_elemt(dados, tipo):
    t = tipo
    requiresAttributes = []
    damageType = []
    defenceType = []
    scalesWith = []
    dmgNegation = []
    resistance = []
    stats = []
    attack = []
    final = {}
    for key in dados.keys():
        if "sub" == key:
            t = dados["sub"]
        elif "req_" in key:
            requiresAttributes.append(cria_dic(dados[key],key))
        elif "dmg_" in key:
            damageType.append(cria_dic(dados[key],key))
        elif "dfc_" in key:
            defenceType.append(cria_dic(dados[key],key))
        elif "neg_" in key:
            dmgNegation.append(cria_dic(dados[key],key))
        elif "res_" in key:
            resistance.append(cria_dic(dados[key],key))
        elif "stats_" in key:
            stats.append(cria_dic(dados[key],key))
        elif "atck_" in key:
            attack.append(cria_dic(dados[key],key))
        elif "scl_" in key:
            val = cria_dic_scal(dados[key],key)
            if val:
                scalesWith.append(val)
        else:
            if dados[key]:
                final[key] = dados[key]
    for lista, nome in [(requiresAttributes,"requiresAttributes"), (dmgNegation,"dmgNegation"), (damageType,"damageType"), (defenceType,"defenceType"), (scalesWith,"scalesWith"), (resistance,"resistance"), (stats,"stats"), (attack,"attack")]:
        if lista:
            final[nome] = json.dumps(lista)
    final["tipo"] = t
    return final        

def create_query(dados):
    uri = re.sub(r'\W+', '_', dados['name'].lower())
    tipo = dados['tipo']
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
insert data{
''' 
    sparql_query += f":{uri} a :{tipo};"
    end = []
    for key in dados.keys():
        value = dados[key].replace("'", "\\'")
        if key != "tipo":
            if "_n" in key:
                new_key = key.replace("_n","")
                end.append(f"\n:{value} :{new_key} :{uri}.")
            elif "_p" in key:
                new_key = key.replace("_p","")
                sparql_query += f"\n:{new_key} :{value};"
            else:
                sparql_query += f"\n:{key} '{value}';"
    sparql_query = sparql_query[:-1] + '.'
    for linha in end:
        sparql_query += linha
    sparql_query += '}'
    print(sparql_query)
    return sparql_query
        
def del_entry(item_uri):
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>

DELETE {{
    :{item_uri} ?o ?p .
}}
WHERE {{
    :{item_uri} ?o ?p .
}}'''
    sparql_query_maker(sparql_query)