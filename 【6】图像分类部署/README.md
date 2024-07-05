>【6】图像分类部署  

@[TOC](文章目录)

---

# 前言
包括将训练好的模型部署在本地终端、web端、小程序上、qt界面化。

---


![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/7df1300cbe2245368db122452850dbba.png)


# 一、将pytorch模型转为ONNX

> 因为mobilenet模型在GPU上训练得到，要使其在CPU 上进行模型推理，需要确保模型的权重被正确地加载到CPU上。

然后再将获得的在CPU上进行推理的pytorch模型转化为ONNX模型。并可使用Netron可视化模型结构。

# 二、本地终端部署
## 2.1. ONNX Runtime部署

> 使用推理引擎ONNX Runtime，读取onnx格式的模型文件，对单张图像、视频进行预测。

## 2.2. pytorch模型部署（补充）

> 不将.pth模型文件转化为onnx模型文件，而是直接部署pytorch模型文件
# 三、使用flask的web网页部署
> flask+bootstrap+jquery+mysql搭建三叶青在线识别网站，使用nginx+gunicorn将网站部署在腾讯云上，配置SSL证书。网站地址：https://www.whtuu.cn

参考我的另外一篇文章：[使用flask的web网页部署介绍](https://blog.csdn.net/2301_78630677/article/details/139707588)
# 四、微信小程序部署

> 利用uniapp+微信开发者工具+flask后端开发了三叶青图像识别微信小程序。

参考我的另外一篇文章：[微信小程序部署](https://blog.csdn.net/2301_78630677/article/details/139708263)
# 五、使用pyqt界面化部署

> pyqt+opencv开发的图像识别qt界面
目前共有五个主要界面：软件介绍界面、省份识别、浙产识别、产地识别界面、以及自定义识别页面。

参考我的另外一篇文章：[使用pyqt界面化部署](https://blog.csdn.net/2301_78630677/article/details/139708598)

---

# 总结
本文主要介绍了如何将pytorch模型转为ONNX模型文件以及如何将图像识别模型部署，包括部署在本地、部署在web网页、小程序、qt界面部署。

2024/6/13