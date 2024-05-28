import requests

CLIENT_ID = "2005031361"
CLIENT_SECRET = "1d96fa3d36b1d56deffd17bb0c5c6a1c"
token_url = "https://api.line.me/oauth2/v2.1/token"
profile_url = "https://api.line.me/v2/profile"
def getLineTokenByRequest(request):
    try:
        code = request.GET.get('code')
        redirect_uri = request.GET.get('liffRedirectUri')
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(token_url, data=payload, headers=headers)
        token_data = response.json()
        access_token = token_data['access_token']
        if access_token != None:
            request.session['line_access_token'] = access_token
        return access_token
    except:
        return None

def getLineUserUidByToken(access_token):
    profile_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile_response = requests.get(profile_url, headers=profile_headers)
    profile_data = profile_response.json()
    return profile_data['userId'] if 'userId' in profile_data else None