from typing import Optional
import requests
import json
import html
import dotenv
import os
from promptdesk.chain import Chain
from promptdesk.JSONMapper import JSONMapper
import cachetools.func
from pybars import Compiler

jmap = JSONMapper()
compiler = Compiler()

cache_ttl = os.getenv("PROMPTDESK_CACHE_TTL", 60*60)

class PromptDesk:
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 service_url: Optional[str] = None,
                 path: Optional[str] = './promptdesk',
                 env: Optional[dict] = {},
                 local: Optional[bool] = False) -> None:
        """
        Initialize the PromptDesk object with API key and service URL.
        :param api_key: API key for PromptDesk, default is taken from environment variable.
        :param service_url: Service URL for PromptDesk, default is taken from environment variable.
        """
        self.api_key = api_key or os.getenv("PROMPTDESK_API_KEY")
        self.service_url = service_url or os.getenv("PROMPTDESK_SERVICE_URL", "https://app.promptdesk.ai")
        self.chain = None
        self.local = local
        self.path = path
        self.env = env

        #remove trailing slash from path
        if self.service_url[-1] == "/":
            self.service_url = self.service_url[:-1]

        #if local, create path in directory
        if self.local:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            #if /{path}/prompts not exists, create it
            if not os.path.exists(f"{self.path}/prompts"):
                os.makedirs(f"{self.path}/prompts")
            if not os.path.exists(f"{self.path}/models"):
                os.makedirs(f"{self.path}/models")

    def ping(self) -> Optional[str]:
        """
        Ping the PromptDesk service to check its availability.
        :return: Response text if successful, None otherwise.
        """
        try:
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.get(f"{self.service_url}/api/ping", headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                text = response.text
                try:
                    text = json.loads(text)
                    text = text['message']
                except:
                    pass
                raise Exception("Failed:", response.status_code, text)
        except requests.RequestException as e:
            raise Exception(f"Service not found: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def convert_to_obj(self, string):
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
        
    def get_prompt(self, prompt_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        response = requests.get(f"{self.service_url}/api/prompt/name/{prompt_name}", headers=headers)
        if response.status_code == 200:
            prompt_object = response.json()
            #save prompt to file
            with open(f"{self.path}/prompts/{prompt_name}.json", "w") as f:
                f.write(json.dumps(prompt_object, indent=4))
            return prompt_object
        else:
            #load prompt from file
            with open(f"{self.path}/prompts/{prompt_name}.json", "r") as f:
                return json.load(f)

    def get_model(self, modelId):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        response = requests.get(f"{self.service_url}/api/model/{modelId}", headers=headers)
        if response.status_code == 200:
            model_object = response.json()
            #save model to file
            with open(f"{self.path}/models/{modelId}.json", "w") as f:
                f.write(json.dumps(model_object, indent=4))
            return model_object
        else:
            #load model from file
            with open(f"{self.path}/models/{modelId}.json", "r") as f:
                return json.load(f)

    def set_api_env(self, api_call, env):
        if env == None:
            env = self.env
        #stringify api
        api_call = json.dumps(api_call)
        #replace {{VARIABLE}} in api with env[VARIABLE]
        for key in env:
            api_call = api_call.replace(f"{{{{{key}}}}}", env[key])
        #parse api back to object
        return json.loads(api_call)
    
    def set_prompt_variables(self, prompt_data, variables):
        prompt_data = json.dumps(prompt_data)
        template = compiler.compile(prompt_data)
        prompt_data = template(variables)
        return json.loads(prompt_data)

    def process_local(self, prompt_name, variables, env):
        prompt = self.get_prompt(prompt_name)
        model = self.get_model(prompt['model'])
        api_call = self.set_api_env(model['api_call'], env)
        prompt_data = self.set_prompt_variables(prompt['prompt_data'], variables)
        if 'prompt_parameters' in prompt:
            prompt_data['model_parameters'] = prompt['prompt_parameters']
        prompt_data = jmap.apply_mapping(prompt_data, model['request_mapping'])
        response = self.process_local_api_call(api_call, prompt_data)
        response = jmap.apply_mapping(response, model['response_mapping'])
        if 'text' in response:
            response = response['text']
        return {
            "message": response
        }
    
    def process_local_api_call(self, api_call, prompt_data):
        response = requests.post(api_call['url'], data=json.dumps(prompt_data), headers=api_call['headers'])
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": True, "message": f"Failed: {response.status_code} {response.text}"}
        
    @cachetools.func.ttl_cache(ttl=cache_ttl, maxsize=1000)
    def cached_call(self, payload, headers):
        payload = json.loads(payload)
        payload['cache'] = True
        return requests.post(f"{self.service_url}/api/generate", data=json.dumps(payload), headers=json.loads(headers))

    def generate(self, prompt_name, variables=None, chain=None, object=False, cache=False, classification=None, env=None):

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
            elif self.local:
                response = self.process_local(prompt_name, variables, env)
            else:
                response = requests.post(f"{self.service_url}/api/generate", data=json.dumps(payload), headers=headers)

            if response.status_code != 200:
                try:
                    text = response.json()
                    text = text['message']
                except:
                    text = response.text
                raise Exception("Failed", response.status_code, text)

            response = response.json()
        
            message = response['message']

            #check if message is string
            if type(message) == str:
                generated_string = message
            elif 'content' in message:
                generated_string = message['content']
            else:
                raise Exception("Failed to generate output - content or message not found in response.")

            if object:
                return self.convert_to_obj(generated_string)
            
            default_classification = {
                True: ["yes", "true", "1"],
                False: ["no", "false", "0"]
            }
            
            if classification:

                if classification == True:
                    classification = default_classification

                for key in classification:
                    for value in classification[key]:
                        if value in generated_string.strip().lower():
                            return key
                return None

            return generated_string

        except requests.RequestException as e:
            raise Exception("Failed to connect:", e)

        except Exception as e:
            raise Exception("An error occurred:", e, response)