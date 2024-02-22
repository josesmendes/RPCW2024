import json

f = open("db.json")
bd = json.load(f)
f.close

instrumentos = {}
def setup_instruments(file):
    ttl = ""
    instrumentos_bd = bd["instrumentos"]
    for ind in instrumentos_bd:
        nome_instrumento = ind["#text"].replace(" ", "_")
        instrumento = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{nome_instrumento}
:{nome_instrumento} rdf:type owl:NamedIndividual ,
                   :Instrumento ;
          :eTocadoPor {instrumentos[nome_instrumento]} ;
          :id_instrumento "{ind["id"]}" ;
          :nome_instrumento "{ind["#text"]}" .
"""
        ttl += instrumento
    file.write(ttl)

def generate_ttl(file):
    ttl = ""
    alunos_bd = bd["alunos"]
    for ind in alunos_bd:
        nome_correto = ind["nome"].replace(" ", "_")
        nome_instrumento = ind["instrumento"].replace(" ", "_")
        aluno = f"""
###  http://rpcw.di.uminho.pt/2024/musica/{nome_correto}
:{nome_correto} rdf:type owl:NamedIndividual ,
                           :Aluno ;
                  :estaNoCurso :{ind["curso"]} ;
                  :toca :{nome_instrumento} ;
                  :ano_curso "{ind["anoCurso"]}" ;
                  :data_nascimento "{ind["dataNasc"]}" ;
                  :id_aluno "{ind["id"]}" ;
                  :nome "{ind["nome"]}" .
"""
        gera_dict(instrumentos, nome_correto, nome_instrumento)
        ttl += aluno
    file.write(ttl)

def gera_curso(file):
    ttl = ""
    cursos_bd = bd["cursos"]
    for ind in cursos_bd:
        nome_instrumento = ind["instrumento"]["#text"].replace(" ", "_")
        curso = f"""
###  http://rpcw.di.uminho.pt/2024/musica/{ind["id"]}
:{ind["id"]} rdf:type owl:NamedIndividual ,
              :Curso ;
     :ensina :{nome_instrumento} ;
     :designacao_curso "{ind["designacao"]}" ;
     :duracao_curso "{ind["duracao"]}"^^xsd:int ;
     :id_curso "{ind["id"]}" .
"""
        ttl += curso
    file.write(ttl)


def gera_dict(dic, indiv, var):
    if var in dic:
        string = dic[var]
        string = f":{indiv},\n" + string
        dic[var] = string
    else:
        dic[var] = f":{indiv}"

if __name__ == "__main__":
    f = open("tpc_output.ttl", "w")
    generate_ttl(f)
    setup_instruments(f)
    gera_curso(f)
