def api_classificador(texto):
    import requests

    url = "https://api-ouvidoria.herokuapp.com/classificacao"

    payload = [{'texto': f"{texto}"}]
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = str(payload))

    return response.text.encode('utf8')
