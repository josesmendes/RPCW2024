import json

f = open("mapa-virtual.json")
bd = json.load(f)
f.close

distritos = {}
def setup_distritos(file, nome_distrito, plain_nome):
    ttl = ""
    distrito = f"""###  http://rpcw.di.uminho.pt/2024/mapa#{nome_distrito}
:{nome_distrito} rdf:type owl:NamedIndividual ,
                     :Distrito ;
            :nome_distrito "{plain_nome}" .
"""
    distritos[nome_distrito] = plain_nome
    file.write(distrito)

def gera_ligação(file):
    ttl = ""
    ligacoes = bd["ligacoes"]
    for ind in ligacoes:
        aluno = f"""###  http://rpcw.di.uminho.pt/2024/mapa#{ind["id"]}
:{ind["id"]} rdf:type owl:NamedIndividual ,
             :Ligacoes ;
    :temDestino :{ind["destino"]} ;
    :temOrigem :{ind["origem"]} ;
    :distancia "{ind["distância"]}"^^xsd:float ;
    :id_ligação "{ind["id"]}" .
"""
        ttl += aluno
    file.write(ttl)

def gera_cidade(file):
    ttl = ""
    cidades = bd["cidades"]
    for ind in cidades:
        nome_distrito = ind["distrito"].replace(" ", "_")
        if nome_distrito not in distritos:
            setup_distritos(file, nome_distrito, ind["distrito"])
        cidade = f"""
###  http://rpcw.di.uminho.pt/2024/mapa#{ind["id"]}
:{ind["id"]} rdf:type owl:NamedIndividual ,
              :Cidades ;
     :pertenceA :{nome_distrito} ;
     :descrição "{ind["descrição"]}" ;
     :id_cidade "{ind["id"]}" ;
     :nome "{ind["nome"]}" ;
     :população "{ind["população"]}"^^xsd:int .
"""
        ttl += cidade
    file.write(ttl)


if __name__ == "__main__":
    f = open("tpc_output.ttl", "w")
    gera_cidade(f)
    gera_ligação(f)
    f.close()
