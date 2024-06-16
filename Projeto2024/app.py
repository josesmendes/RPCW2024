import json
import re
from aux import *
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import requests


app = Flask(__name__)


graphdb_endpoint = "http://localhost:7200/repositories/elden_ring"

data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')
    


@app.route('/')
def index():
    if request.method == 'POST':
        print(request.form["item_type"])
    return render_template('index.html')

########## ITEMS ###########
@app.route('/items')
def items():
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?subclass WHERE {
  ?subclass rdfs:subClassOf er:Items .
}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        subclasses = [{'subclass': item['subclass']['value']} for item in dados]
        return render_template('items.html', data=subclasses)
    else:
        print(f"Error fetching items: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/items/<subclass>', methods=['GET', 'POST'])
def items_subclasse(subclass):
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?item ?name ?img WHERE {{
  ?item rdf:type er:{subclass} ;
        er:name ?name .
  OPTIONAL {{ ?item er:image ?img . }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        items = [{'item': item['item']['value'], 'name': item['name']['value'], 'img': item.get('img', {}).get('value', None)} for item in dados]
        return render_template('items_subclass.html', subclass=subclass, data=items)
    else:
        print(f"Error fetching items for subclass {subclass}: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/items/<subclass>/<item>')
def item_detail(subclass, item):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?img ?name ?desc ?effect ?boss ?boss_name WHERE {{
    er:{item} er:image ?img ;
              er:name ?name ;
              er:description ?desc ;
              er:effect ?effect .
              optional{{
        ?boss er:Drops er:{item};
              er:name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        if dados:
            new_dados = boss_list(dados)
            details = {
                'img': new_dados[0].get('img', {}).get('value', None),
                'name': new_dados[0].get('name', {}).get('value', None),
                'desc': new_dados[0].get('desc', {}).get('value', None),
                'effect': new_dados[0].get('effect', {}).get('value', None),
                'boss': new_dados[0].get('boss', {}).get('value',None)
            }
            return render_template('item_detail.html', data={'type': (subclass, item), 'details': details})
        else:
            print("No data found for item.")
            return render_template('empty.html', data={'data': data_iso_formatada})
    else:
        print(f"Error fetching details for item {item}: {resposta.status_code}")
        print(resposta.text)
        return render_template('empty.html', data={'data': data_iso_formatada})

########### INCANTATIONS #########
    
@app.route('/incantations', methods=['GET', 'POST'])
def incantations():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>

SELECT DISTINCT ?incantation ?name ?img WHERE {
  ?incantation rdf:type er:Incantations ;
               er:name ?name .
  OPTIONAL { ?incantation er:image ?img . }
}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        incantations = [{'uri': item['incantation']['value'], 'name': item['name']['value'], 'img': item.get('img', {}).get('value', None)} for item in dados]
        return render_template('incantations.html', data={'type': 'Incantations', 'incantations': incantations})
    else:
        print(f"Error fetching incantations: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/incantations/<incantation>')
def incantation_detail(incantation):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?img ?name ?desc ?cost ?slots ?effects ?requires ?boss ?boss_name WHERE {{
    er:{incantation} er:image ?img ;
                      er:name ?name ;
                      er:description ?desc ;
                      er:fpCost ?cost ;
                      er:slots ?slots ;
                      er:effect ?effects ;
                      er:requiresAttributes ?requires .
        optional{{
        ?boss er:Drops er:{incantation};
              er:name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        if dados:
            # Ajustar a string JSON dos requisitos
            requires = dados[0].get('requires', {}).get('value', '[]')
            requires = requires.replace("'", '"')
            try:
                requires = json.loads(requires)
            except json.JSONDecodeError:
                requires = []
            
            details = {
                'img': dados[0].get('img', {}).get('value', None),
                'name': dados[0].get('name', {}).get('value', None),
                'desc': dados[0].get('desc', {}).get('value', None),
                'cost': dados[0].get('cost', {}).get('value', None),
                'slots': dados[0].get('slots', {}).get('value', None),
                'effects': dados[0].get('effects', {}).get('value', None),
                'boss': dados[0].get('boss', {}).get('value', None),
                'boss_name': dados[0].get('boss_name', {}).get('value', None),
                'requires': requires
            }
            return render_template('incantation_detail.html', data={'type': incantation, 'details': details})
        else:
            print("No data found for incantation.")
            return render_template('empty.html', data={'data': data_iso_formatada})
    else:
        print(f"Error fetching details for incantation {incantation}: {resposta.status_code}")
        print(resposta.text)
        return render_template('empty.html', data={'data': data_iso_formatada})

############  LOCATIONS  ##############

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?location ?name ?img WHERE {
  ?location rdf:type er:Location ;
            er:name ?name .
  OPTIONAL { ?location er:image ?img . }
}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        locations = [{'uri': item['location']['value'], 'name': item['name']['value'], 'img': item.get('img', {}).get('value', None)} for item in dados]
        return render_template('locations.html', data={'type': 'Locations', 'locations': locations})
    else:
        print(f"Error fetching locations: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/locations/<location>')
def location_detail(location):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?img ?name ?desc ?region ?region_name WHERE {{
    er:{location} er:image ?img ;
                  er:name ?name ;
                  er:description ?desc ;
                  er:isInRegion ?region .
    ?region er:name ?region_name .
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        if dados:
            details = {
                'img': dados[0].get('img', {}).get('value', None),
                'name': dados[0].get('name', {}).get('value', None),
                'desc': dados[0].get('desc', {}).get('value', None),
                'region': dados[0].get('region', {}).get('value', None),
                'region_name': dados[0].get('region_name', {}).get('value', None)
            }
            return render_template('location_detail.html', data={'type': location, 'details': details})
        else:
            print("No data found for location.")
            return render_template('empty.html', data={'data': data_iso_formatada})
    else:
        print(f"Error fetching details for location {location}: {resposta.status_code}")
        print(resposta.text)
        return render_template('empty.html', data={'data': data_iso_formatada})

################# REGIONS #################

@app.route('/regions', methods=['GET', 'POST'])
def regions():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?region ?name WHERE {
  ?region rdf:type er:Region ;
          er:name ?name .
}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        regions = [{'region': item['region']['value'], 'name': item['name']['value']} for item in dados]
        return render_template('regions.html', data=regions)
    else:
        print(f"Error fetching regions: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/regions/<region>')
def region_detail(region):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?name ?boss ?boss_name WHERE {{
    er:{region} er:name ?name .
    OPTIONAL {{
        ?boss er:isInRegion er:{region} ;
              rdf:type er:Boss ;
              er:name ?boss_name .
    }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        if dados:
            details = {
                'name': dados[0].get('name', {}).get('value', None),
                'bosses': [{'uri': item['boss']['value'], 'name': item['boss_name']['value']} for item in dados if 'boss' in item]
            }
            return render_template('region_detail.html', data={'type': region, 'details': details})
        else:
            print("No data found for region.")
            return render_template('empty.html', data={'data': data_iso_formatada})
    else:
        print(f"Error fetching details for region {region}: {resposta.status_code}")
        print(resposta.text)
        return render_template('empty.html', data={'data': data_iso_formatada})


############ NPCS ###########

@app.route('/npcs', methods=['GET', 'POST'])
def npcs():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?npc ?name ?img WHERE {
  ?npc rdf:type er:Npcs ;
       er:name ?name .
  OPTIONAL { ?npc er:image ?img . }
}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        npcs = [{'uri': item['npc']['value'], 'name': item['name']['value'], 'img': item.get('img', {}).get('value', None)} for item in dados]
        return render_template('npcs.html', data={'type': 'Npcs', 'npcs': npcs})
    else:
        print(f"Error fetching npcs: {resposta.status_code}")
        return render_template('empty.html')

@app.route('/npcs/<npc>')
def npc_detail(npc):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX er: <http://rpcw.di.uminho.pt/2024/eldenring/>
SELECT DISTINCT ?name ?desc ?img ?role ?location WHERE {{
    er:{npc} er:name ?name ;
              er:image ?img ;
              er:role ?role .
    OPTIONAL {{ er:{npc} er:isInLocation ?location . }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={'query': sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        if dados:
            details = {
                'name': dados[0].get('name', {}).get('value', None),
                'img': dados[0].get('img', {}).get('value', None),
                'role': dados[0].get('role', {}).get('value', None),
                'location': dados[0].get('location', {}).get('value', None)
            }
            return render_template('npc_detail.html', data={'type': npc, 'details': details})
        else:
            print("No data found for npc.")
            return render_template('empty.html', data={'data': data_iso_formatada})
    else:
        print(f"Error fetching details for npc {npc}: {resposta.status_code}")
        print(resposta.text)
        return render_template('empty.html', data={'data': data_iso_formatada})

#sparql_query = f'''
#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
#select distinct ?s where {{ 
#	:albinauric_bow :damageType ?s .
#}}
#'''
#resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
#if resposta.status_code == 200:
#    dados = resposta.json()['results']['bindings']
#    print(dados[0]["s"]["value"])
#    #render_template('grupo.html', data = dados)
#else:
#    print("hello")
#    #render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/weapons')
def weapons():
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?weapon_type where { 
	?weapon_type rdfs:subClassOf :Weapons ;
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('weapons.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/weapons/<weapon_type>', methods=['GET', 'POST'])
def weapons_type(weapon_type):
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?weapon ?img ?name where {{ 
	?weapon a :{weapon_type} ;
         :name ?name;
    optional{{?weapon :image ?img.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('weapon_type.html', data = { 'type': weapon_type, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/weapons/<weapon_type>/<weapon>')
def weapon(weapon_type, weapon):
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?dmg_t ?dfc_t ?desc ?img ?name ?requires ?scales ?wght ?boss ?boss_name where {{
        :{weapon} :damageType ?dmg_t.
        :{weapon} :defenceType ?dfc_t.
        :{weapon} :description ?desc.
        :{weapon} :name ?name.
        :{weapon} :requiresAttributes ?requires.
        :{weapon} :scalesWith ?scales.
        :{weapon} :weight ?wght.        
        :{weapon} :image ?img.
        optional{{
        ?boss :Drops :{weapon};
              :name ?boss_name.
    }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["dmg_t", "dfc_t", "requires", "scales"]
        new_dados = turn_to_json(dados,lista)
        return render_template('weapon.html', data = { 'type': (weapon_type,weapon), 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/shields')
def shields():
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?shield_type where { 
	?shield_type rdfs:subClassOf :Shields.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('shields.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/shields/<shields_type>', methods=['GET', 'POST'])
def shields_type(shields_type):
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?shield ?img ?name where {{ 
	?shield a :{shields_type} ;
         :name ?name;
         :image ?img.
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('shield_type.html', data = { 'type': shields_type, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/shields/<shields_type>/<shield>')
def shield(shields_type, shield):
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?dmg_t ?dfc_t ?desc ?img ?name ?requires ?scales ?wght where {{
        :{shield} :damageType ?dmg_t.
        :{shield} :defenceType ?dfc_t.
        :{shield} :description ?desc.
        :{shield} :name ?name.
        :{shield} :requiresAttributes ?requires.
        :{shield} :scalesWith ?scales.
        :{shield} :weight ?wght.        
        :{shield} :image ?img
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["dmg_t", "dfc_t", "requires", "scales"]
        new_dados = turn_to_json(dados,lista)
        return render_template('shield.html', data = { 'type': (shields_type, shield), 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })



@app.route('/sorceries', methods=['GET', 'POST'])
def sorceries():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Sorceries;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('sorceries.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/sorceries/<sorcerie>')
def sorcerie(sorcerie):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?eft ?cost ?req ?slots ?boss ?boss_name where {{
    :{sorcerie} :name ?name;
           :image ?img;
           :description ?desc;
           :effect ?eft;
           :fpCost ?cost;
           :requiresAttributes ?req;
           :slots ?slots.
    optional{{
        ?boss :Drops :{sorcerie};
              :name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["req"]
        new_dados = turn_to_json(dados,lista)
        return render_template('sorcerie.html', data = { 'type': sorcerie, 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/spirits', methods=['GET', 'POST'])
def spirits():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Spirits;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('spirits.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/spirits/<spirit>')
def spirit(spirit):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?eft ?fp_cost ?hp_cost ?boss ?boss_name where {{
    :{spirit} :name ?name;
           :image ?img;
           :description ?desc;
           :effect ?eft;
           :fpCost ?fp_cost;
           :hpCost ?hp_cost.
    optional{{
        ?boss :Drops :{spirit};
              :name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('spirit.html', data = { 'type': spirit, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/talismans', methods=['GET', 'POST'])
def talismans():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Talismans;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('talismans.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/talismans/<talisman>')
def talisman(talisman):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?eft ?boss ?boss_name where {{
    :{talisman} :name ?name;
           :image ?img;
           :description ?desc;
           :effect ?eft.
    optional{{
        ?boss :Drops :{talisman};
              :name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('talisman.html', data = { 'type': talisman, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/armors')
def armors():
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?armor_type where { 
	?armor_type rdfs:subClassOf :Armors.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('armors.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/armors/<armors_type>', methods=['GET', 'POST'])
def armors_type(armors_type):
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?armor ?img ?name where {{ 
	?armor a :{armors_type} ;
         :name ?name;
         :image ?img.
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('armor_type.html', data = { 'type': armors_type, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/armors/<armors_type>/<armor>')
def armor(armors_type, armor):
    sparql_query = f'''
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?dmg_neg ?res ?desc ?img ?name ?wght ?boss ?boss_name where {{
        :{armor} :dmgNegation ?dmg_neg.
        :{armor} :resistance ?res.
        :{armor} :description ?desc.
        :{armor} :name ?name.
        :{armor} :weight ?wght.        
        :{armor} :image ?img
        optional{{
        ?boss :Drops :{armor};
              :name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["dmg_neg", "res"]
        new_dados = turn_to_json(dados,lista)
        return render_template('armor.html', data = { 'type': (armors_type, armor), 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/ashes', methods=['GET', 'POST'])
def ashes():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Ashes;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('ashes.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/ashes/<ash>')
def ash(ash):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?aff ?hab ?boss ?boss_name where {{
    :{ash} :name ?name;
           :image ?img;
           :description ?desc;
           :affinity ?aff;
           :skill ?hab.
    optional{{
        ?boss :Drops :{ash};
              :name ?boss_name.}}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('ash.html', data = { 'type': ash, 'data': dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })







@app.route('/classes', methods=['GET', 'POST'])
def classes():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Classes;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('classes.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })


@app.route('/classes/<clas>')
def clas(clas):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?stats where {{
    :{clas} :name ?name;
            :image ?img;
            :description ?desc;
            :stats ?stats.
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["stats"]
        new_dados = turn_to_json(dados,lista)
        return render_template('clas.html', data = { 'type': clas, 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })



@app.route('/ammos', methods=['GET', 'POST'])
def ammos():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Ammos;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('ammos.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })
    

@app.route('/ammos/<ammo>')
def ammo(ammo):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?pass ?atk where {{
    :{ammo} :name ?name;
            :image ?img;
            :description ?desc;
            :passive ?pass;
            :attack ?atk.
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        lista = ["atk"]
        print(dados)
        new_dados = turn_to_json(dados,lista)
        return render_template('ammo.html', data = { 'type': ammo, 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })










@app.route('/bosses', methods=['GET', 'POST'])
def bosses():
    if request.method == 'POST':
        del_entry(request.form["item_uri"])
    sparql_query = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?s ?name ?img where {
        ?s rdf:type :Boss;
           :name ?name;
           :image ?img.
}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('bosses.html', data = dados)
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })
    

@app.route('/bosses/<boss>')
def boss(boss):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?name ?img ?desc ?region ?location ?hp ?runes ?drops ?type ?drop_name ?uper where {{
    :{boss} :name ?name;
            :image ?img;
            :description ?desc;
            :healthPoints ?hp;
            :drops ?runes.
    optional {{:{boss} :Drops ?drops.
    	?drops rdf:type ?type.
        ?drops :name ?drop_name.
        optional{{?type rdfs:subClassOf ?uper}}}}
    optional{{
        :{boss} :isInRegion ?region.
        }}
    optional{{
        :{boss} :isInLocation ?location.
    }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        new_dados = concat_eq(dados)
        return render_template('boss.html', data = { 'type': boss, 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/new_element')
def new_element():
    return render_template('new_element.html')

@app.route('/new_element/<tipo>', methods=['GET', 'POST'])
def new_weapon(tipo):
    sparql_query = f'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/eldenring/>
select distinct ?p ?n ?sub where {{
    ?s  rdf:type :{tipo};
   		?p ?o.
    optional{{
        ?x ?n ?s.
    }}
    optional{{
        ?sub rdfs:subClassOf :{tipo}.
    }}
}}
'''
    resposta = requests.get(graphdb_endpoint, params={ 'query': sparql_query }, headers={ 'Accept': 'application/sparql-results+json' })
    if resposta.status_code == 200:
        if request.method == 'POST':
            query = create_query(insert_elemt(request.form.to_dict(), tipo))
            sparql_query_maker(query)
            return redirect(url_for('new_element'))
        dados = resposta.json()['results']['bindings']
        new_dados = limpa_tipos(dados)
        if "n" in new_dados.keys():
            d = get_values(new_dados["n"], "n")
            for keys, vals in d.items():
                new_dados[keys] = vals
        if "prop" in new_dados.keys():
            d = get_values(new_dados["prop"], "p")
            for keys, vals in d.items():
                new_dados[keys] = vals
        return render_template('new_entity/maker.html', data = { 'type': tipo, 'data': new_dados })
    else:
        return render_template('empty.html', data = { 'data': data_iso_formatada })

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        print(request.form["item_type"])
    return ("nothing")


if __name__ == '__main__':
    app.run(debug=True)
