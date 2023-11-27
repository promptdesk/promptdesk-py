from typing import Optional
import requests
import json
import html
import dotenv
import os
from promptdesk.chain import Chain
import cachetools.func
cache_ttl = os.getenv("PROMPTDESK_CACHE_TTL", 60*60)

class PromptDesk:
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 service_url: Optional[str] = None) -> None:
        """
        Initialize the PromptDesk object with API key and service URL.
        :param api_key: API key for PromptDesk, default is taken from environment variable.
        :param service_url: Service URL for PromptDesk, default is taken from environment variable.
        """
        self.api_key = api_key or os.getenv("PROMPTDESK_API_KEY")
        self.service_url = service_url or os.getenv("PROMPTDESK_SERVICE_URL", "https://app.promptdesk.ai")
        self.chain = None


    def ping(self) -> Optional[str]:
        """
        Ping the PromptDesk service to check its availability.
        :return: Response text if successful, None otherwise.
        """
        try:
            response = requests.get(f"{self.service_url}/ping")
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed: {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def convert_to_obj(self, string):
        """
        Convert a string to an object.
        :param string: String to be converted.
        """
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

    def list(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        response = requests.get(f"{self.service_url}/api/prompts", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed:", response.status_code, response.text)
        
    @cachetools.func.ttl_cache(ttl=cache_ttl, maxsize=1000)
    def cached_call(self, payload, headers):
        payload = json.loads(payload)
        payload['cache'] = True
        return requests.post(f"{self.service_url}/api/generate", data=json.dumps(payload), headers=json.loads(headers))

    def generate(self, prompt_name, variables=None, chain=None, object=False, cache=False):

        payload = {
            "prompt_name": prompt_name,
            "variables": variables or {}
        }

        if chain:
            payload["chain"] = {
                "uuid": chain.uuid,
                "name": chain.name
            }

        if self.api_key == None:
            raise Exception("API_KEY is not set")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        try:
            response = None

            if cache:
                response = self.cached_call(json.dumps(payload), json.dumps(headers))
            else:
                response = requests.post(f"{self.service_url}/api/generate", data=json.dumps(payload), headers=headers)

            message = response.json()['message']

            #check if message is string
            if type(message) == str:
                generated_string = message
            elif 'content' in message:
                generated_string = message['content']
            else:
                raise Exception("Failed to generate output")

            if object:
                return self.convert_to_obj(generated_string)
            else:
                return generated_string

        except requests.RequestException as e:
            # Handle connection errors
            raise Exception("Failed to connect:", e)

        except Exception as e:
            # Handle other types of exceptions
            raise Exception("An error occurred:", response.json())