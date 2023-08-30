import openrouteservice

coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key='5b3ce3597851110001cf624867c98a0c9b584886ae412e203ca81a4e') # Specify your personal API key
routes = client.directions(coords)

print(routes)