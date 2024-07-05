#将三叶青的块根空白与非空白背景照片混合
import os
import shutil
import pandas as pd
def hunhe_sanyeqing(source_folder_bai, source_folder_fei, target_folder, labels_csv, labels_feibai_csv):
    # 读取标签文件
    labels_bai = pd.read_csv(labels_csv,encoding='utf-8')
    labels_fei = pd.read_csv(labels_feibai_csv,encoding="utf-8")

    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 准备一个列表来存储图片的ID和标签
    labels = []

    # 遍历源文件夹及其所有子文件夹中的文件
    for i, bai_file in enumerate(labels_bai['ID']):
        for dirpath, dirnames, filenames in os.walk(source_folder_bai):
            if f"{bai_file}.png" in filenames:
                # 复制并重命名图片文件
                shutil.copy(os.path.join(dirpath, f"{bai_file}.png"), os.path.join(target_folder, f"{i}.png"))
                # 记录图片的ID和标签
                labels.append((i, labels_bai.loc[i, 'labels']))
                break

    for i, fei_file in enumerate(labels_fei['ID']):
        for dirpath, dirnames, filenames in os.walk(source_folder_fei):
            if f"{fei_file}.png" in filenames:
                # 复制并重命名图片文件
                shutil.copy(os.path.join(dirpath, f"{fei_file}.png"), os.path.join(target_folder, f"{i+len(labels_bai)}.png"))
                # 记录图片的ID和标签
                labels.append((i+len(labels_bai), labels_fei.loc[i, 'labels']))
                break

    # 将图片的ID和标签保存到CSV文件中
    df = pd.DataFrame(labels, columns=["ID", "labels"])
    df.to_csv(os.path.join(target_folder, "labels_hun.csv"), index=False)




def labels_to_custom(source_file, destination_file):
    # 创建一个字典来映射原始标签和新标签
    label_dict = {
        "GXBS": "广西省",
        "GXGL": "广西省",
        "GXYL": "广西省",
        "GZBJ": "贵州省",
        "GZQXN": "贵州省",
        "SXXA": "陕西省",
        'YNKM': '云南省',
        "YNXSBN": "云南省",
        "ZJTZ": "浙江省",
        "ZJWZ": "浙江省",
        '未知': '未知',  # 处理未知的标签
    }

    df = pd.read_csv(source_file)
    df['labels'] = df['labels'].apply(lambda x: label_dict.get(x, '未知'))
    df.to_csv(destination_file, index=False)


if __name__ == '__main__':
    # source_folder_bai = "D:\\三叶青项目\\wht-sanyeqing\\"
    # source_folder_fei = "D:\\三叶青项目\\非纯白——wht-sanyeqing\\"
    # target_folder = r"D:\三叶青项目\混合——wht-sanyeqing\train_hun"
    # labels_csv = "D:\三叶青项目\wht-sanyeqing\labels.csv"
    # labels_feibai_csv = "D:\三叶青项目\非纯白——wht-sanyeqing\labels_feibai.csv"
    # hunhe_sanyeqing(source_folder_bai, source_folder_fei, target_folder, labels_csv, labels_feibai_csv)

    hunhe_sanyeqing(source_folder_bai="D:\\SanYeQing_Project\\hunhe-wht-sanyeqing\\train_hun_400",
                    source_folder_fei="D:\\train_weizhi_yasuo",
                    target_folder="D:\\SanYeQing_Project\\hunhe-wht-sanyeqing\\train_hun_weizhi",
                    labels_csv="D:\SanYeQing_Project\hunhe-wht-sanyeqing\labels_hun.csv",
                    labels_feibai_csv="D:\labels_weizhi.csv")

    labels_to_custom(source_file=r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\train_hun_weizhi\labels_hun.csv",destination_file=r"D:\SanYeQing_Project\hunhe-wht-sanyeqing\train_hun_weizhi\labels_hun1.csv")






