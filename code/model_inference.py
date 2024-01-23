from openai import OpenAI
import base64
import settings
# from settings import OPENAI_API_KEY, OPENAI_MODEL_NAME, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, WEBSIGHT_MODEL_NAME, QWENVL_MODEL_NAME
from src.i2hBaseline.VLM_websight.VLM_websight_api import generateAnswer_websight
from src.i2hBaseline.Qwen_VL.qwen_vl import generateAnswer_qwen_vl
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class ModelInference:
    def __init__(self, model=settings.OPENAI_MODEL_NAME):
        self.model = model

    def infer(self, image_path):
        match self.model:
            case settings.OPENAI_MODEL_NAME:
                return self.infer_with_openai(image_path)
            case settings.WEBSIGHT_MODEL_NAME:
                return self.infer_with_websight(image_path)
            case settings.QWENVL_MODEL_NAME:
                return self.infer_with_qwenvl(image_path)
            case _:
                pass
 

    def infer_with_openai(self, image_path):
        # We currently support PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif).
        image = Image.open(image_path)
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
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )
        print(response)
        return response.choices[0].message.content

    def infer_with_qwenvl(self, image_path):
        # 实现Qwen-VL的调用
        return generateAnswer_qwen_vl(image_path=image_path)

    def infer_with_websight(self, image_path):
        # https://huggingface.co/HuggingFaceM4/VLM_WebSight_finetuned
        return generateAnswer_websight(image_path=image_path)


# input_data = '/Users/knediny/html/Image2HTML-Benchmark/code/test/google.png'
input_data = '/Users/yisuanwang/Desktop/image2html/Image2HTML-Benchmark/code/src/i2hBaseline/VLM_websight/google.png'
model_inference = ModelInference(settings.WEBSIGHT_MODEL_NAME)
model_inference = ModelInference(settings.QWENVL_MODEL_NAME)
inference_html = model_inference.infer(input_data)
print(inference_html)
