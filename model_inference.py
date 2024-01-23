from openai import OpenAI
import base64
from settings import OPENAI_API_KEY, OPENAI_MODEL_NAME, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class ModelInference:
    def __init__(self, model=OPENAI_MODEL_NAME):
        self.model = model

    def infer(self, input_data):
        match self.model:
            case OPENAI_MODEL_NAME:
                return self.infer_with_openai(input_data)

    def infer_with_openai(self, text, image):
        # We currently support PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif).
        base64_image = encode_image(image)
        client = OpenAI(
            api_key=OPENAI_API_KEY
        )
        response = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                # "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                                "detail": "auto",  # "auto", "low", "high",
                            },
                        },
                    ],
                }
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )
        print(response)
        return response.choices[0].message.content

    def infer_with_qwenvl(self, input_data):
        # 实现Qwen-VL的调用
        return "Qwen-VL的推理结果"


input_data = '/Users/knediny/html/Image2HTML-Benchmark/code/test/google.png'
model_inference = ModelInference(OPENAI_MODEL_NAME)
inference_html = model_inference.infer(input_data)
print(inference_html)
