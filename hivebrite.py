import requests
from settings import settings


def get_token() -> str:

    url = f"{settings.base_url}/oauth/token"

    data = {
        'grant_type': settings.grant_type,
        'scope': settings.scope,
        'admin_email': settings.admin_email,
        'password': settings.password,
        'client_id': settings.client_id,
        'client_secret': settings.client_secret,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Assuming the response contains JSON data
        json_data = response.json()
        access_token = json_data.get('access_token')
        print(f"Access token: {access_token}")
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
    return


def update_user(user_id, cv_path = None, hs_path = None,  ):

    url = f"{settings.base_url}/admin/v1/users/{user_id}"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {settings.token}'
    }

    if not cv_path and not hs_path:
        raise ValueError(f"no files for {user_id}")

    files = {}

    if cv_path:
        files['user[resume]'] = open(cv_path, 'rb')

    if hs_path:
        files['user[photo]'] =  open(hs_path, 'rb')

    r = requests.put(url, headers=headers, files=files)

    for file in files.values():
        file.close()

    return r.status_code == 200
