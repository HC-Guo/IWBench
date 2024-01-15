import pdb

from .service import Service

generation_config = dict(
    max_new_tokens=2048,
    repetition_penalty=1.1,
)

from dataclasses import dataclass

import time
import openai

api_key = "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" # image2html

openai.api_key = api_key

def parse_openai_object_to_plain_response(openai_object, model_name):
    if model_name == 'davinci-003':
        return openai_object['choices'][0]['text']
    elif model_name in ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4']:
        return openai_object['choices'][0]['message']['content']
    else:
        raise ValueError(f'model: {model_name} not found')


@dataclass
class Client:
    api_key: str


class OpenaiService:
    def __init__(self, model_name):
            self.model_name = model_name

    def make_request(self, prompt, plain_text=True):
        while True:
            try:
                response = self._send_request(prompt)
                if plain_text:
                    return parse_openai_object_to_plain_response(response, self.model_name)
                else:
                    return response
            except Exception as e:
                    print(f'Openai Error: {e}')
                    print('sleep 5 second ...')
                    time.sleep(5)

    def _send_request(self, prompt):
        if self.model_name in ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo', 'gpt-4']:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
               ]
            )
        else:
            response = openai.Completion.create(
                model=self.model_name,
                prompt=prompt
            )
        return response



# service = OpenaiService('gpt-3.5-turbo')
# input = '''
# You are a HTML Comparator. Your description is API-style HTML comparison, returns JSON. The HTML Comparator is tailored for users who are familiar with API interactions, specifically resembling an OpenAI API-like interface. It processes requests in a structured format, typically as a POST request with two HTML files or their contents. The GPT then analyzes these files, identifying differences in structure, style, content, and more, and returns a detailed JSON object with the comparison results. In cases of errors, such as missing files or invalid HTML, it provides an error message in JSON format. The communication style of HTML Comparator is concise, technical, and mimics API documentation, guiding users on request formatting and response interpretation.
# '''
# res = service.make_request(input)
# print(res)


