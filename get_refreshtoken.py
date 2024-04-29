import requests
from urllib.parse import urlencode
import webbrowser
import base64

# Defina as configurações do seu app Spotify
CLIENT_ID = '13316762f31e4cf3ae0b89fe485d05e8'
CLIENT_SECRET = 'dd25db3db38c4739ab65f5d93637c371'
REDIRECT_URI = 'http://localhost:3000'


# Construa a URL para solicitar o código
auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
    "response_type": "code",
    "client_id": CLIENT_ID,
    "scope": "user-library-read user-library-modify user-top-read user-read-private user-library-read",  # Altere conforme as permissões necessárias
    "redirect_uri": REDIRECT_URI
})

# Abra a URL no navegador
webbrowser.open(auth_url)

# Captura o código que foi retornado após a autenticação e autorização
auth_code = input("Entre o código de autenticação da URL: ")

# Solicite o access token e refresh token usando o código
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': REDIRECT_URI
}
# Codifique Client ID e Client Secret em Base64 para a autenticação
client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

token_headers = {
    'Authorization': f'Basic {client_creds_b64}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(token_url, data=token_data, headers=token_headers)
token_info = response.json()

# Exiba o access token e refresh token
print("Access Token:", token_info.get('access_token'))
print("Refresh Token:", token_info.get('refresh_token'))


