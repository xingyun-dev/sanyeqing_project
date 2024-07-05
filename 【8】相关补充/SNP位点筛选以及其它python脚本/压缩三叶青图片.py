from PIL import Image
import os

def resize_images(source_dir, target_dir, max_width, max_height, target_size=None):
    """
    Resize images in a directory and save them to another directory.

    :param source_dir: The directory of the original images.
    :param target_dir: The directory to save the resized images.
    :param max_width: The maximum width of the resized images.
    :param max_height: The maximum height of the resized images.
    :param target_size: The target size of the resized images. If specified, the images will be resized to this size.
    """
    # 确保目标文件夹存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_dir):
        # 检查文件是否是图片（你可以根据需要添加其他格式）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # 构建源文件和目标文件的完整路径
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)

            try:
                # 打开图片
                with Image.open(source_path) as img:
                    if target_size:  # 强制压缩
                        # 裁剪或缩放图片以适应目标尺寸
                        img_resized = img.resize(target_size)
                        img_resized.save(target_path)
                    else:
                        # 获取原始图片的宽度和高度
                        width, height = img.size
                        # 计算新的尺寸，保持长宽比
                        if width > height:
                            new_width = max_width
                            new_height = int(height * (max_width / width))
                        else:
                            new_height = max_height
                            new_width = int(width * (max_height / height))
                            # 调整图片大小并保持长宽比
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                        # 保存调整后的图片到目标文件夹
                        img.save(target_path)

                    # 打印进度信息（可选）
                print(f"Resized and copied {filename} to {target_dir}")
            except Exception as e:
                # 打印错误信息并继续处理其他文件
                print(f"Error processing {filename}: {e}")

    print("Resizing and copying completed.")


if __name__ == '__main__':
    # 原始图片文件夹路径
    source_dir = r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\test_hun"
    # 目标文件夹路径，调整大小后的图片将被复制到这里
    target_dir = r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\test_hun_400"
    # 指定的图片宽度和高度(保持原始图片的长宽比进行压缩）
    max_width = 400
    max_height = 400
    target_size = None
    # target_size = (400, 400)  # 强制压缩为640×640
    resize_images(source_dir, target_dir, max_width,max_height, target_size)





# # 确保目标文件夹存在
# if not os.path.exists(target_dir):
#     os.makedirs(target_dir)
#
# # 遍历源文件夹中的所有文件
# for filename in os.listdir(source_dir):
#     # 检查文件是否是图片（你可以根据需要添加其他格式）
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
#         # 构建源文件和目标文件的完整路径
#         source_path = os.path.join(source_dir, filename)
#         target_path = os.path.join(target_dir, filename)
#
#         try:
#             # 打开图片
#             with Image.open(source_path) as img:
#                 if target_size:  # 强制压缩
#                     # 裁剪或缩放图片以适应目标尺寸
#                     img_resized = img.resize(target_size)
#                     img_resized.save(target_path)
#                 else:
#                     # 获取原始图片的宽度和高度
#                     width, height = img.size
#                     # 计算新的尺寸，保持长宽比
#                     if width > height:
#                         new_width = max_width
#                         new_height = int(height * (max_width / width))
#                     else:
#                         new_height = max_height
#                         new_width = int(width * (max_height / height))
#                         # 调整图片大小并保持长宽比
#                     img = img.resize((new_width, new_height), Image.LANCZOS)
#                     # 保存调整后的图片到目标文件夹
#                     img.save(target_path)
#
#                 # 打印进度信息（可选）
#             print(f"Resized and copied {filename} to {target_dir}")
#         except Exception as e:
#             # 打印错误信息并继续处理其他文件
#             print(f"Error processing {filename}: {e}")
#
# print("Resizing and copying completed.")
