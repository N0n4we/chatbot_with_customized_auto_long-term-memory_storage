import requests
import json
import time
from utils import try_decorator
from string import Template
from config import revisorConfig, thinkerConfig, performerConfig

class Client:
    def __init__(self, model_name, api_key, base_url, completionOptions, max_retries=3, retry_delay=1):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.completionOptions = completionOptions
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    @try_decorator
    def parse_response(self, response):
        response = response.json()
        responseMessage = response["choices"][0]["message"]
        return responseMessage

    def make_request(self, messages, retry_count=0):
        try:
            response = requests.post(
                url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-type": "application/json"
                },
                data=json.dumps({
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": self.completionOptions.temperature,
                    "max_tokens": self.completionOptions.max_tokens,
                    "top_p": self.completionOptions.top_p,
                    "min_p": self.completionOptions.min_p,
                    "top_k": self.completionOptions.top_k,
                    "frequency_penalty": self.completionOptions.frequency_penalty,
                    "presence_penalty": self.completionOptions.presence_penalty
                }),
                timeout=30  # Add 30 second timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout as e:
            print(f"\nRequest timed out (attempt {retry_count + 1}/{self.max_retries})")
            if retry_count < self.max_retries:
                time.sleep(self.retry_delay * (retry_count + 1))
                return self.make_request(messages, retry_count + 1)
            raise Exception(f"Request failed after {self.max_retries} retries: {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed (attempt {retry_count + 1}/{self.max_retries}): {str(e)}")
            if retry_count < self.max_retries:
                time.sleep(self.retry_delay * (retry_count + 1))
                return self.make_request(messages, retry_count + 1)
            raise Exception(f"Request failed after {self.max_retries} retries: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"\nJSON decode error (attempt {retry_count + 1}/{self.max_retries})")
            if retry_count < self.max_retries:
                time.sleep(self.retry_delay * (retry_count + 1))
                return self.make_request(messages, retry_count + 1)
            raise Exception(f"JSON decode error after {self.max_retries} retries: {str(e)}")

    # responseMessage = {'role': 'assistant', 'content': '$reply'}
    @try_decorator
    def request(self, messages):
        response = self.make_request(messages)
        responseMessage = self.parse_response(response)
        return responseMessage

    @try_decorator
    def revise(self, template, systemPrompt=None, **args):
        messages = []
        if systemPrompt:
            messages.append({"role": "system", "content": systemPrompt})
        messages.append({"role": "user", "content": Template(template).substitute(args)})
        
        response = self.make_request(messages)
        responseMessage = self.parse_response(response)
        return responseMessage


revisor = Client(revisorConfig.model_name, revisorConfig.api_key, revisorConfig.base_url, revisorConfig.completionOptions)
thinker = Client(thinkerConfig.model_name, thinkerConfig.api_key, thinkerConfig.base_url, thinkerConfig.completionOptions)
performer = Client(performerConfig.model_name, performerConfig.api_key, performerConfig.base_url, performerConfig.completionOptions)
