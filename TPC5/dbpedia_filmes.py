import requests, json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"
movies_data = []
num = 0
for counter in range(200):
    offset = counter * 1000
    print(f"EXTRAÇÃO NUM {counter}")
    # Define the SPARQL query
    sparql_query = f"""
    select distinct ?movie ?label ?nameWriter ?nameMusic ?nameDiretor ?nameArgumentista (GROUP_CONCAT(?nameActors; separator=", ") AS ?actors)  where {{
?movie a <http://schema.org/Movie>;
 rdfs:label ?label.
optional {{ 
?movie dbo:writer ?writer.
?writer dbp:name ?nameWriter.
}}
optional {{ 
?movie dbo:musicComposer ?music.
?music dbp:name ?nameMusic.
}}
optional {{ 
?movie dbo:cinematography ?argumentista.
?argumentista dbp:name ?nameArgumentista.
}}
optional {{
?movie dbo:director ?diretor.
?diretor dbp:name ?nameDiretor}}
optional {{
?movie dbo:starring ?atores.
?atores dbp:name ?nameActors.}}

filter(lang(?label) = 'en')
}}
GROUP BY  ?movie ?label ?nameWriter ?nameMusic ?nameDiretor ?nameArgumentista
limit 1000 offset {offset}
    """

    # Define the headers
    headers = {
        "Accept": "application/sparql-results+json"
    }

    # Define the parameters
    params = {
        "query": sparql_query,
        "format": "json"
    }

    # Send the SPARQL query using requests
    response = requests.get(sparql_endpoint, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        # Print the results
        for result in results["results"]["bindings"]:
            num += 1
            movie_info = {}
            movie_info["uri"] = result["movie"]["value"]
            movie_info["nome"] = result["label"]["value"]
            if 'nameWriter' in result.keys():
                movie_info["escritor"] = result["nameWriter"]["value"]
            if 'nameMusic' in result.keys():
                movie_info["musico"] = result["nameMusic"]["value"]
            if 'actors' in result.keys():
                movie_actors = result["actors"]["value"]
                movie_info["atores"] = movie_actors.split(",")
            if 'nameArgumentista' in result.keys():
                movie_info["argumentista"] = result["nameArgumentista"]["value"]
            if 'nameDiretor' in result.keys():
                movie_info["diretor"] = result["nameDiretor"]["value"]
                # Create a dictionary for the current result

            # Append the current result dictionary to the list
            movies_data.append(movie_info)
    else:
        print("Error:", response.status_code)
        print(response.text)
# Define the path for the output .json file
output_file_path = "movies.json"

# Write the data to the .json file
with open(output_file_path, "w") as json_file:
    json.dump(movies_data, json_file, indent=4)
print(f"num of movies found: {num}")
print("Data has been written to:", output_file_path)

