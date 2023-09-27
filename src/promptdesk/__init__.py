import requests
import json
import html

SERVICE_URL = "http://localhost:4000"

def ping():

    response = requests.get(f"{SERVICE_URL}/ping")

    if response.status_code == 200:
        return response.text
    else:
        print("Failed:", response.status_code, response.text)

def convert_to_obj(string):
    string = html.unescape(string)
    string = string.strip()
    last = string[-1]
    try:
        try:
            r = json.loads(string)
            return r
        except:
            r = eval(string)
            return r
    except:
        if last == "]":
            return []
        elif last == "}":
            return {}
        else:
            return None

def generate(prompt_name, variables=None, object=False):
    payload = {
        "prompt_name": prompt_name,
        "variables": variables or {}
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{SERVICE_URL}/api/magic/generate", data=json.dumps(payload), headers=headers)
        
        # Check for HTTP errors
        if response.status_code != 200:
            print("Failed:", response.status_code, response.json()['error'])
            return
        
        generated_string = response.json()['data']['message']['content']

        if object:
            return convert_to_obj(generated_string)
        else:
            return generated_string
        
    except requests.RequestException as e:
        # Handle connection errors
        print("Failed to connect:", e)
        
    except Exception as e:
        # Handle other types of exceptions
        print("An error occurred:", e)