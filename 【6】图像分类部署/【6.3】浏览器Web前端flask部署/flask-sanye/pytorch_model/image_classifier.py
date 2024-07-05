from pytorch_model.AipImageClassify import __classify
from pytorch_model.AipImageClassify_ye import __classify_ye
def get_imgGeneral(type, image):
    if (type == 0):
        return __classify(image)
    elif (type == 1):
        return __classify_ye(image)
    else:
        return "类型或图片格式错误"

