> 使用flask的web网页部署介绍

@[TOC](文章目录)

---
# 前言
flask+bootstrap+jquery+mysql搭建三叶青在线识别网站，使用nginx+gunicorn将网站部署在腾讯云上，配置SSL证书。网站地址：[https://www.whtuu.cn](https://www.whtuu.cn)

---
# 一、网页介绍

> 网页的界面主要包括登录界面、首页、在线识别、历史记录、个人中心、图片库以及其它界面。
> （如果看过我之前的博客，会发现其实这个网站的很多前端页面都是我之前自己搭建的学习网站——星云小窝 的页面，为了快速开发这个网站，我就直接拿了之前的代码并修改了一下。）
> 之前自己搭建的学习网站介绍:
> [星云小窝项目1.0——项目介绍（一）](https://blog.csdn.net/2301_78630677/article/details/136622251?spm=1001.2014.3001.5502)

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/b100a88e0a1949408074f2c8bc96ff35.png)


![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/70301867b15848e7b4bfaf46a0784b9c.png)


![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/b7b5680449a94d1fb802bb37bf8f9bed.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/51246f4bd27a4a8e9b920828a441066c.png)


![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/9efe90733d1e488594b92bf711cd17e0.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/288e7863bf7341b68ba444fbf64d74dd.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/253278228ca84436aad35f8f045e4716.png)


# 二、数据库设计介绍

> 这个网站我就简单的只设计三张表：ecode（验证码存放表）、photos（图片表）、users（用户表）
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/3c6dcf67e76b433ba65e68afea8f2bba.png)


其中，users表是基础的，用于存放网站的注册用户，存储用户注册的id、邮箱、密码，昵称、头像、身份、创建时间、介绍。
photos表，则是存放注册用户提交的图片，
至于ecode表，则是临时存放邮箱地址以及验证码，用于在手机端小程序中的注册，因为在小程序端没有session，无法像网页一样存储验证码，而小程序上只能通过生成token后，从后端的数据库中获取验证码。故我设计了这一个表格，用于小程序从后端获取验证码，并且定时删除表中的内容。


---

# 总结
本文主要介绍了使用flask搭建的三叶青在线识别网站，同时也简单介绍了数据库的设计

2024/6/12

