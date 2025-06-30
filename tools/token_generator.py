import requests

def get_facebook_token(cookies):
    url = "https://www.facebook.com/yuvi001x"
    params = {'cookies': cookies}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': f"API request failed with status code {response.status_code}",
                'details': response.json()
            }
    except requests.exceptions.RequestException:
        return {
            'error': "Failed to connect to the API server",
            'details': "Network or server issue."
        }
    except ValueError as e:
        return {
            'error': "Invalid JSON response from server",
            'details': str(e)
        }
