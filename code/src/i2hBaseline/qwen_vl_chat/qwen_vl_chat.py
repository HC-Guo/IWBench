from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch

def generateAnswer_qwen_vl_chat(device='cuda', model_path = "Qwen/Qwen-VL-chat", text='Generate html source code corresponding to the image:', image_path='https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'):
    torch.manual_seed(1234)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True).eval()

    # Specify hyperparameters for generation (No need to do this if you are using transformers>=4.32.0)
    # model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)

    query = tokenizer.from_list_format([
    #   Either a local path or an u[](https://)rl between <img></img> tags.
        {'image': image_path},
        {'text': text},
    ])
    inputs = tokenizer(query, return_tensors='pt')
    inputs = inputs.to(model.device)
    pred = model.generate(**inputs)
    response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=False)
    # print(response)
    return response
    
    # # <img>https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg</img>Generate the caption in English with grounding:<ref> Woman</ref><box>(451,379),(731,806)</box> and<ref> her dog</ref><box>(219,424),(576,896)</box> playing on the beach<|endoftext|>
    # image = tokenizer.draw_bbox_on_latest_picture(response)
    # if image:
    #     image.save('2.jpg')
    # else:
    #     print("no box")
