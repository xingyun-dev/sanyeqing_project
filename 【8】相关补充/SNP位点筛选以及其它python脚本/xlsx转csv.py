import pandas as pd

# 读取XLSX文件
xlsx_file = "D:\三叶青项目\wht-sanyeqing\idx_to_labels.xlsx"
df = pd.read_excel(xlsx_file, engine='openpyxl')
#
# # 将DataFrame转换为CSV并指定UTF-8编码
# csv_file = 'D:\三叶青项目\三叶青根部照片——整理省份\labels.csv'
# df.to_csv(csv_file, index=False, encoding='utf-8')
# csv = "D:\三叶青项目\wht-sanyeqing\idx_to_labels.csv"
# df = pd.read_csv(csv,encoding='gbk')

# 将DataFrame转换为CSV并指定UTF-8编码
csv_file = "D:\三叶青项目\wht-sanyeqing\idx_to_labels1.csv"
df.to_csv(csv_file, index=False, encoding='utf-8')


