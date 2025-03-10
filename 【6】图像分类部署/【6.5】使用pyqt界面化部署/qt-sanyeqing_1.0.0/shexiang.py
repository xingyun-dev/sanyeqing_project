import json
import os

import onnxruntime
import torch
from torchvision import transforms
import torch.nn.functional as F
import numpy as np
from PIL import Image, ImageFont, ImageDraw
# 调用摄像头逐帧实时处理模板
import cv2
import time

from tqdm import tqdm

from sanye_pred_chan import device


def load_model_and_labels(model_path, labels_json_path):
    # 检查模型文件的扩展名
    _, ext = os.path.splitext(model_path)
    if ext == '.onnx':
        # 加载 onnx 模型
        model = onnxruntime.InferenceSession(model_path)
    elif ext == '.pth':
        # 加载 PyTorch 模型
        model = torch.load(model_path, map_location=device)  # 或者使用 torch.load，取决于你的模型是如何保存的
    else:
        raise ValueError("Unknown model file extension")

    # 加载标签
    with open(labels_json_path, 'r', encoding='utf-8') as f:
        labels = json.load(f)

    return model, labels



# 测试时，我们只使用确定性的图像预处理操作
transform_test = transforms.Compose([transforms.Resize(256),
                                     # 从图像中心裁切224x224大小的图片
                                     transforms.CenterCrop(224),
                                     transforms.ToTensor(),
                                     transforms.Normalize([0.485, 0.456, 0.406],
                                                          [0.229, 0.224, 0.225])
                                     ])


# 处理帧函数
def process_frame(img, n, ort_session, labels):
    '''
    输入摄像头拍摄画面bgr-array，输出图像分类预测结果bgr-array
    '''

    # 记录该帧开始处理的时间
    start_time = time.time()

    ## 画面转成 RGB 的 Pillow 格式
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR转RGB
    img_pil = Image.fromarray(img_rgb)  # array 转 PIL

    ## 预处理
    input_img = transform_test(img_pil)  # 预处理
    # input_tensor = input_img.unsqueeze(0).numpy()
    input_tensor = input_img.unsqueeze(0)
    ## 判断模型类型并进行预测
    if isinstance(ort_session, torch.nn.Module):
        # 使用 PyTorch 进行预测
        with torch.no_grad():
            ort_session.eval()
            input_tensor = input_tensor.to(device)
            pred_logits = ort_session(input_tensor)
            pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算
    elif isinstance(ort_session, onnxruntime.InferenceSession):
        # 使用 ONNX Runtime 进行预测
        input_tensor = input_tensor.numpy()
        ort_inputs = {'input': input_tensor}  # onnx runtime 输入
        pred_logits = ort_session.run(['output'], ort_inputs)[0]  # onnx runtime 输出
        pred_logits = torch.tensor(pred_logits)
        pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算
    else:
        raise ValueError("Unknown model type")
    #
    # 获取类别的数量
    num_classes = n

    # 如果类别数小于等于11，则显示所有类别，否则只显示前11个
    if num_classes <= 11:
        top_n = torch.sort(pred_softmax, descending=True)
    else:
        top_n = torch.topk(pred_softmax, 11)  # 取置信度最大的 11 个结果
    pred_ids = top_n[1].cpu().detach().numpy().squeeze()  # 解析出类别
    confs = top_n[0].cpu().detach().numpy().squeeze()  # 解析出置信度

    from PIL import ImageFont

    # 加载字体，第二个参数是字体大小
    font = ImageFont.truetype('simsun.ttc', 15)

    ## 在图像上写中文
    draw = ImageDraw.Draw(img_pil)
    # 获取类别的数量
    num_classes = len(confs)

    # 如果类别数小于等于11，则显示所有类别，否则只显示前11个
    if num_classes <= 11:
        display_classes = num_classes
    else:
        display_classes = 11

    for i in range(display_classes):
        class_name = labels[str(pred_ids[i])]  # 获取类别名称
        text = '{:<15} {:>.3f}'.format(class_name, confs[i])
        # 文字坐标，中文字符串，字体，rgba颜色
        draw.text((50, 100 + 30 * i), text, fill=(255,0 ,255 , 1), font=font)
    img = np.array(img_pil)  # PIL 转 array
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # RGB转BGR

    # 记录该帧处理完毕的时间
    end_time = time.time()
    # 计算每秒处理图像帧数FPS
    FPS = 1 / (end_time - start_time)
    # 图片，添加的文字，左上角坐标，字体，字体大小，颜色，线宽，线型
    img = cv2.putText(img, 'FPS  ' + str(int(FPS)), (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 4,
                      cv2.LINE_AA)
    return img


def generate_video(input_path, n, ort_session,labels):
    filehead = input_path.split('/')[-1]
    output_path = "out-" + filehead
    #
    # print('视频开始处理', input_path)

    # 获取视频总帧数
    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while cap.isOpened():

        success, frame = cap.read()
        frame_count += 1
        if not success:
            break
    cap.release()
    # print('视频总帧数为', frame_count)
    cap = cv2.VideoCapture(input_path)
    # print(cap)
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (int(frame_size[0]), int(frame_size[1])))
    # print(out)
    # 进度条绑定视频总帧数
    with tqdm(total=frame_count - 1) as pbar:
        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                try:
                    frame = process_frame(img=frame, n=n, ort_session=ort_session, labels=labels)
                except:
                    # print('报错！', os.error)
                    pass

                if success == True:
                    cv2.imshow('Video Processing', frame)
                    out.write(frame)

                    # 进度条更新一帧
                    pbar.update(1)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except:
            # print('中途中断')
            pass

    cv2.destroyAllWindows()
    out.release()
    cap.release()
    # print('视频已保存', output_path)


# # 加载初始模型和标签
# ort_session, labels = load_model_and_labels('./model_cpu_3.onnx', './class_indices_2.json')
# # 获取摄像头，传入0表示获取系统默认摄像头
# cap = cv2.VideoCapture(0)
# # 打开cap
# cap.open(0)
# # 无限循环，直到break被触发
# while cap.isOpened():
#     # 获取画面
#     success, frame = cap.read()
#     if not success:
#         print('Error')
#         break
#
#         # 使用当前模型和标签处理帧
#     frame = process_frame(frame, 11, ort_session, labels)
#
    # # 展示处理后的三通道图像
    # cv2.imshow('my_window', frame)
    #
    # # 如果用户长按下 '1'，则切换到模型1和标签1
    # if cv2.waitKey(1) == ord('a'):
    #     ort_session, labels = load_model_and_labels('./model_cpu_97.18.onnx', './class_indices_5.json')
    #
    # # 如果用户长按下 '2'，则切换到模型2和标签2
    # elif cv2.waitKey(1) == ord('s'):
    #     ort_session, labels = load_model_and_labels('./model_cpu_3.onnx', './class_indices_2.json')
    #
    # # 如果用户长按下 '3'，则切换到模型3和标签3
    # elif cv2.waitKey(1) == ord('d'):
    #     ort_session, labels = load_model_and_labels('./model_cpu_11.onnx', './class_indices_10.json')
    #
    # # 如果用户长按下 'q' 或 'esc'，则退出循环
    # elif cv2.waitKey(1) in [ord('q'), 27]:
    #     break
# # 关闭摄像头
# cap.release()
# # 关闭图像窗口
# cv2.destroyAllWindows()
