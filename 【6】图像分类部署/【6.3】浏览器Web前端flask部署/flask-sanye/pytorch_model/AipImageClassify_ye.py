import os
import io
import json
# import onnxruntime
import torch
import torchvision.transforms as transforms
from PIL import Image

# weights_path = "./pytorch_model/resnet152_sanyeqing_weizhi_6_1_zheng.pth"
weights_path = "./pytorch_model/model_cpu_97.18.pth"
class_json_path = "./pytorch_model/class_indices.json"
assert os.path.exists(weights_path), "weights path does not exist..."
assert os.path.exists(class_json_path), "class json path does not exist..."

# select device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.load(weights_path, map_location=device)
model.to(device)
model.eval()
# load class info
json_file = open(class_json_path, 'rb')
class_indict = json.load(json_file)
def transform_image(image_bytes):
    img_size = 224
    my_transforms = transforms.Compose([transforms.Resize(int(img_size * 1.143)),
                                        transforms.CenterCrop(img_size),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        # raise ValueError("input file does not RGB image...")
        image = image.convert("RGB")
    return my_transforms(image).unsqueeze(0).to(device)


def get_prediction_img(image_bytes):
    try:
        tensor = transform_image(image_bytes=image_bytes)
        outputs = torch.softmax(model.forward(tensor).squeeze(), dim=0)
        prediction = outputs.detach().cpu().numpy()
        # print(prediction)
        index_pre = [(class_indict[str(index)], float(p)) for index, p in enumerate(prediction)]
        index_pre.sort(key=lambda x: x[1], reverse=True)
        # 将结果转换为(name, score)对的列表
        result_list = [{"name": k, "score": v} for k, v in index_pre]
        return {"result": result_list}
    except Exception as e:
        return {"result": [{"error": str(e)}]}



""" 调用叶片图像 """
def __classify_ye(image):
    info = get_prediction_img(image_bytes=image)
    # print(info)
    return info




