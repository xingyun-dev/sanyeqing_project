import os
import random
import shutil
def random_select_images(source_folder, target_folder, ratio):
    # 遍历源文件夹及其子文件夹，收集图片文件
    images = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                images.append(os.path.join(root, file))

    # 计算需要选择的图片数量
    num_images = int(len(images) * ratio)

    # 随机挑选指定数量的图片
    selected_images = random.sample(images, num_images)

    # 将挑选出的图片复制到目标文件夹，保留文件名
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for image in selected_images:
        # 获取图片文件名（不包含路径）
        filename = os.path.basename(image)
        # 构造目标文件路径
        target_path = os.path.join(target_folder, filename)
        # 移动文件到目标路径
        shutil.move(image, target_path)

    return selected_images


if __name__ == '__main__':
    # 使用示例
    source_folder = r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\train_hun_weizhi"  # 源文件夹路径
    target_folder = r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\test_hun_weizhi"  # 目标文件夹路径
    ratio = 0.2  # 需要挑选的图片比例
    random_select_images(source_folder, target_folder, ratio)




#
#
# def random_select_images(source_folder, target_folder, num_images):
#     # 遍历源文件夹及其子文件夹，收集图片文件
#     images = []
#     for root, dirs, files in os.walk(source_folder):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
#                 images.append(os.path.join(root, file))
#
#                 # 如果图片数量少于所需数量，则直接返回所有图片
#     if len(images) < num_images:
#         return images
#
#         # 随机挑选指定数量的图片
#     selected_images = random.sample(images, num_images)
#
#     # 将挑选出的图片复制到目标文件夹，保留文件名
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)
#     for image in selected_images:
#         # 获取图片文件名（不包含路径）
#         filename = os.path.basename(image)
#         # 构造目标文件路径
#         target_path = os.path.join(target_folder, filename)
#         # 移动文件到目标路径
#         shutil.move(image, target_path)
#
#     return selected_images
#
#
# if __name__ == '__main__':
#     # 使用示例
#     source_folder = r"D:\三叶青项目\混合——wht-sanyeqing\train_hun"  # 源文件夹路径
#     target_folder = r"D:\三叶青项目\混合——wht-sanyeqing\test_hun"  # 目标文件夹路径
#     num_images = 600  # 需要挑选的图片数量
#     random_select_images(source_folder, target_folder, num_images)


