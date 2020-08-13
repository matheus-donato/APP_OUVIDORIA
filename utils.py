def api_classificador(texto,endpoint,tema=None):
    import requests

    #url = "https://api-ouvidoria.herokuapp.com/classificacao"
    url = f"http://127.0.0.1:5000/{endpoint}"
    payload = {}
    token = get_token()
    if 'temas' in endpoint:

        headers = {
        'texto':texto,
        'tema':tema,
        'Authorization': f'JWT {token}'
        }
    else:
        headers = {
        'texto':texto,
        'Authorization': f'JWT {token}'
        }

    response = requests.request("POST", url, headers=headers, data = str(payload))

    return response.text.encode('utf8')

def get_token():
    import json
    import requests
    url = "http://127.0.0.1:5000/auth"

    payload = {"username": "Inova","password":"inova*mprj1"}
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    response = response.json()
    return response['access_token']