import json

f = open("/home/jose-mendes/Downloads/plantas.json")
bd = json.load(f)
f.close

f = open("tpc_output.ttl", "w")
ttl = ""
freguesias = []
implantacoes = []
gestores = []
ruas = []
especies = []
for planta in bd:
    if planta["Freguesia"] not in freguesias:
        freguesia = f"""###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#{planta["Freguesia"]}
:{planta["Freguesia"]} rdf:type owl:NamedIndividual ,
                      :Freguesia ;
             <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
"""
        ttl += freguesia
        freguesias.append(planta["Freguesia"])

    if planta["Gestor"] not in gestores:
        gestor = f"""###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#{planta["Gestor"]}
:{planta["Gestor"]} rdf:type owl:NamedIndividual ,
               :Gestor ;
      <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
      """
        ttl += gestor
        gestores.append(planta["Gestor"])

    if planta["Implantação"] not in implantacoes:
        implantacao = f"""###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#{planta["Implantação"]}
:{planta["Implantação"]} rdf:type owl:NamedIndividual ,
                     :Implantacao ;
            <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
            """
        ttl += implantacao
        implantacoes.append(planta["Implantação"])
        
    if planta["Rua"] not in ruas:
        rua = f"""###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#{planta["Rua"]}
:{planta["Rua"]} rdf:type owl:NamedIndividual ,
                          :Rua ;
                 <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
                 """
        ttl += rua
        ruas.append(planta["Rua"])

    if planta["Espécie"] not in especies:
        especie = f"""###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#{planta["Espécie"]}
:{planta["Espécie"]} rdf:type owl:NamedIndividual ,
                         :Especie ;
                <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
"""
        ttl += especie
        especies.append(planta["Espécie"])

    if "Sim" in planta["Caldeira"]:
        planta["Caldeira"] = "true"
    elif "Não" in  planta["Caldeira"]:
        planta["Caldeira"] = "false"
    if "Sim" in planta["Tutor"]:
        planta["Tutor"] = "true"
    elif "Não" in  planta["Tutor"]:
        planta["Tutor"] = "false"
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/untitled-ontology-6#20615557
<http://rpcw.di.uminho.pt/2024/untitled-ontology-6#20615557> rdf:type owl:NamedIndividual ,
                                                                      :Planta ;
                                                             :daEspecie :{planta["Espécie"]} ;
                                                             :naFreguesia :{planta["Freguesia"]} ;
                                                             :naRua :{planta["Rua"]} ;
                                                             :temGestor :{planta["Gestor"]} ;
                                                             :tipoImplantacao :{planta["Implantação"]} ;
                                                             :local "{planta["Local"]}" ;
                                                             :codigoRua "{planta["Código de rua"]}" ;
                                                             :nomeCientifico "{planta["Nome Científico"]}" ;
                                                             :caldeira "{planta["Caldeira"]}"^^xsd:boolean ;
                                                             :data "{planta["Data de Plantação"]}" ;
                                                             :dataUpdate "{planta["Data de actualização"]}" ;
                                                             :numIntervencao "{planta["Número de intervenções"]}"^^xsd:int ;
                                                             :numRegisto "{planta["Número de Registo"]}" ;
                                                             :origem "{planta["Origem"]}" ;
                                                             :tutor "{planta["Tutor"]}"^^xsd:boolean ;
                                                             <http://purl.org/dc/elements/1.1/creator> "jose-mendes" .
"""
    ttl += registo
f.write(ttl)
print(ttl)
