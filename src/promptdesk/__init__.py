import requests
import json
import html
import uuid

PUBLIC_SERVICE_URL = "https://app.promptdesk.ai"
SERVICE_URL = None
ORGANIZATION = None
API_KEY = None

if SERVICE_URL == None:
    SERVICE_URL = PUBLIC_SERVICE_URL

def ping():
    response = requests.get(f"{SERVICE_URL}/ping")
    if response.status_code == 200:
        return response.text
    else:
        print("Failed:", response.status_code, response.text)

def convert_to_obj(string):
    if type(string) == dict or type(string) == list:
        return string
    string = html.unescape(string)
    string = string.strip()
    try:
        try:
            r = json.loads(string)
            return r
        except:
            r = eval(string)
            return r
    except:
        return None

def list():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    response = requests.get(f"{SERVICE_URL}/api/prompts", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed:", response.status_code, response.text)

def generate(prompt_name, variables=None, chain=None, object=False):

    payload = {
        "prompt_name": prompt_name,
        "variables": variables or {}
    }

    if chain:
        payload["chain"] = {
            "uuid": chain.uuid,
            "name": chain.name
        }

    if API_KEY == None:
        raise Exception("API_KEY is not set")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }

    if ORGANIZATION:
        headers["Organization"] = ORGANIZATION

    try:
        response = requests.post(f"{SERVICE_URL}/api/magic/generate", data=json.dumps(payload), headers=headers)
        
        message = response.json()['message']

        #check if message is string
        if type(message) == str:
            generated_string = message
        elif 'content' in message:
            generated_string = message['content']
        else:
            raise Exception("Failed to generate output")

        if object:
            return convert_to_obj(generated_string)
        else:
            return generated_string

    except requests.RequestException as e:
        # Handle connection errors
        raise Exception("Failed to connect:", e)

    except Exception as e:
        # Handle other types of exceptions
        raise Exception("An error occurred:", response.json())

class Chain:
    def __init__(self, name) -> None:
        self.uuid = str(uuid.uuid4())
        self.name = name
        pass