import os
import shutil
import pandas as pd


#
# def photo_copy(source_folder, destination_folder, by_region=False):
#     """
#         # 整理三叶青图片（by_region=True,整理到具体地区。默认整理到省份）
#         # source_folder  源文件目录
#         # destination_folder  整理文件目录
#     """
#     listdir = os.listdir(source_folder)
#     df = pd.DataFrame(columns=['ID', 'labels'])
#     counter = 0
#
#     for i in listdir:
#         print(i)
#         listdir_i = os.listdir(os.path.join(source_folder, i))
#         if listdir_i:
#             for j, file in enumerate(listdir_i):
#                 print(j, file)
#                 if by_region:
#                     region = file  # 获取地区名称
#                     listdir_i_j = os.listdir(os.path.join(source_folder, i, file))
#                     for f in listdir_i_j:
#                         source_file = os.path.join(source_folder, i, file, f)
#                         destination_file_name = str(counter) + '.png'
#                         counter += 1
#                         destination_file = os.path.join(destination_folder, i, region, destination_file_name)
#                         os.makedirs(os.path.dirname(destination_file), exist_ok=True)
#                         shutil.copy2(source_file, destination_file)
#                         new_row = pd.DataFrame([[counter - 1, region]], columns=['ID', 'labels'])
#                         df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     listdir_i_j = os.listdir(os.path.join(source_folder, i, file))
#                     for f in listdir_i_j:
#                         source_file = os.path.join(source_folder, i, file, f)
#                         destination_file_name = str(counter) + '.png'
#                         counter += 1
#                         destination_file = os.path.join(destination_folder, i, destination_file_name)
#                         os.makedirs(os.path.dirname(destination_file), exist_ok=True)
#                         shutil.copy2(source_file, destination_file)
#                         new_row = pd.DataFrame([[counter - 1, i]], columns=['ID', 'labels'])
#                         df = pd.concat([df, new_row], ignore_index=True)
#         print(), print()
#         print("*********************************************")
#     df.to_excel('D:\三叶青项目\三叶青根部照片——整理具体\三叶青文件名和标签.xlsx', index=False)
#

#
# if __name__ == '__main__':
#     photo_copy('D:\三叶青项目\正在做——三叶青根部照片', 'D:\三叶青项目\三叶青根部照片——整理具体', by_region=True)


def photo_copy(source_folder, destination_folder, by_region):
    """
    :param source_folder:
    :param destination_folder:
    :param by_region:
    :return:
    """
    listdir = os.listdir(source_folder)
    df = pd.DataFrame(columns=['ID', 'labels'])
    counter = 0

    for i in listdir:
        print(i)
        listdir_i = os.listdir(os.path.join(source_folder, i))
        if listdir_i:
            for j, file in enumerate(listdir_i):
                print(j, file)
                if by_region == "二级目录-按地区名称":
                    region = file  # 获取地区名称
                    listdir_i_j = os.listdir(os.path.join(source_folder, i, file))
                    for f in listdir_i_j:
                        source_file = os.path.join(source_folder, i, file, f)
                        destination_file_name = str(counter) + '.png'
                        counter += 1
                        destination_file = os.path.join(destination_folder, destination_file_name)
                        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                        shutil.copy2(source_file, destination_file)
                        new_row = pd.DataFrame([[counter - 1, region]], columns=['ID', 'labels'])
                        df = pd.concat([df, new_row], ignore_index=True)
                elif by_region == "二级目录-按省份名称":
                    listdir_i_j = os.listdir(os.path.join(source_folder, i, file))
                    for f in listdir_i_j:
                        source_file = os.path.join(source_folder, i, file, f)
                        destination_file_name = str(counter) + '.png'
                        counter += 1
                        destination_file = os.path.join(destination_folder, destination_file_name)
                        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                        shutil.copy2(source_file, destination_file)
                        new_row = pd.DataFrame([[counter - 1, i]], columns=['ID', 'labels'])
                        df = pd.concat([df, new_row], ignore_index=True)
                else:
                    source_file = os.path.join(source_folder, i, file)
                    destination_file_name = str(counter) + '.png'
                    counter += 1
                    destination_file = os.path.join(destination_folder, destination_file_name)
                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                    shutil.copy2(source_file, destination_file)
                    new_row = pd.DataFrame([[counter - 1, i]], columns=['ID', 'labels'])
                    df = pd.concat([df, new_row], ignore_index=True)

        print(), print()
        print("*********************************************")
    df.to_csv(r'D:\labels.csv', index=False)

#
# if __name__ == '__main__':
#     photo_copy(r'D:\weizhi-photo\dataset', r'D:\train_weizhi', by_region=False)





# 根据labels.csv文件整理为labels_2.csv或labels_5.csv或lebels_未知.csv
def labels_to_x(source_file, destination_file, is_lei):
    df = pd.read_csv(source_file)
    if is_lei == 2:
        df['labels'] = df['labels'].apply(lambda x: x[:2] if x[:2] == 'ZJ' else 'not_ZJ')
    elif is_lei == 5:
        df['labels'] = df['labels'].apply(lambda x: x[:2])
    elif is_lei == "未知":
        df['labels'] = df['labels'].apply(lambda x: '未知')
    df.to_csv(destination_file, index=False)

#
# if __name__ == '__main__':
#     labels_to_x("D:\labels.csv", "D:\labels_weizhi.csv",is_lei="未知")
#     print("===================")
    # labels_to_x("D:\三叶青项目\混合——wht-sanyeqing\labels_hun.csv", "D:\三叶青项目\混合——wht-sanyeqing\labels_hun_2.csv",is_2=True)



