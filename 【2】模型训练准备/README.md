
> 【2】模型训练准备



---
# 前言
构建完图像分类数据集后，就要开始训练我们的模型了，深度学习模型训练需要大量计算资源，也就是GPU。
可以在本地机器上使用GPU（如果有的话），或者在云服务上租用GPU资源。此外，还有专门为深度学习训练提供的服务，如Google的Colab和Kaggle。

本文将简单介绍一下如何使用kaggle上的GPU资源。

---
# 一、kaggle账户创建

> 注册完kaggle账号后，为了使用GPU资源，还要进行手机号验证

推荐文章

[https://blog.csdn.net/jiabiao1602/article/details/139370991](https://blog.csdn.net/jiabiao1602/article/details/139370991)

[https://blog.csdn.net/weixin_51288849/article/details/130164188](https://blog.csdn.net/weixin_51288849/article/details/130164188)


# 二、创建kaggle项目

> 由于考虑到kaggle云平台GPU使用时间的限制，我创建了一个kaggle项目让团队成员加入进来，登录他们的账号进行训练。

参考文章：
[如何在kaggle中发布一个项目以便管理](https://blog.csdn.net/2301_78630677/article/details/137529760)



# 三、使用

> 将图像数据上传到kaggle项目中


相关notebook代码,请参见：
kaggle_train.ipynb
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/78098bc53a9d412fa9b1cbc76c05889f.png)



---

# 总结
准备好了模型训练的资源，将数据上传到了kaggle平台，编写了相关代码。

2024/6/12 


共赏金尊沈绿蚁，莫辞醉，此花不与群花比