import csv
def convert_txt_to_csv(txt_file, csv_file):
    with open(txt_file, "r") as file:
        txt_data = file.readlines()
    data = []
    for line in txt_data:
        columns = line.strip().split("\t")

        # 将第一列和第二列拆分为两个列
        ref_alt = columns[0].split()
        columns = ref_alt + columns[1:]
        data.append(columns)

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("转换完成！")


#
txt_file = r"D:\三叶青项目\三叶青项目分享\139.SNP.gt.txt"
csv_file = "139.SNP.csv"
convert_txt_to_csv(txt_file, csv_file)

import pandas as pd

# 读取数据文件
data = pd.read_csv('139.SNP.csv', delimiter=',')
print(data.shape)
# 筛选以"ZJ"开头的列
zj_individuals = data.filter(regex=r'^ZJ.*$', axis=1)
print(zj_individuals.shape)
# 其它剩余个体列
other_individuals = data.drop(zj_individuals.columns, axis=1)
other_individuals = other_individuals.drop(data.columns[:4], axis=1)
print(other_individuals.shape)
# print(other_individuals.head(10))


# 先尝试找出在浙江也就是ZJ开头的个体里面基因型全是1|1 而在其他个体里面是0|0这种位点
zj_filtered01 = data[(zj_individuals == '1|1').all(axis=1)]
print(zj_filtered01.shape)
# print(zj_filtered01.head(10))
other_filtered01 = data[(other_individuals == '0|0').all(axis=1)]
print(other_filtered01.shape)
# 找到交集
filtered_data01 = pd.merge(zj_filtered01, other_filtered01, how='inner')
print(filtered_data01.shape)  # 没有交集

# 或者找出在浙江也就是ZJ开头的个体里面基因型全是0|0 而在其他个体里面是1|1这种位点。
zj_filtered02 = data[(zj_individuals == '0|0').all(axis=1)]
print(zj_filtered02.shape)
other_filtered02 = data[(other_individuals == '1|1').all(axis=1)]
print(other_filtered02.shape)
# 找到交集
filtered_data02 = pd.merge(zj_filtered02, other_filtered02, how='inner')
print(filtered_data02.shape)

# 可以找一下在ZJ里面全是1|1，在其他个体里面没有1|1这种情况
zj_filtered03 = data[(zj_individuals == '1|1').all(axis=1)]
print(zj_filtered03.shape)
# print(zj_filtered03.head(10))
other_filtered03 = data[(other_individuals != '1|1').all(axis=1)]
print(other_filtered03.shape)
# 找到交集
filtered_data03 = pd.merge(zj_filtered03, other_filtered03, how='inner')
print(filtered_data03.shape)
# print(filtered_data03)


# 还可以找一下在ZJ里面是0｜0，在其他个体里面没有0|0的
zj_filtered04 = data[(zj_individuals == '0|0').all(axis=1)]
print(zj_filtered04.shape)
other_filtered04 = data[(other_individuals != '0|0').all(axis=1)]
print(other_filtered04.shape)
# 找到交集
filtered_data04 = pd.merge(zj_filtered04, other_filtered04, how='inner')
print(filtered_data04.shape)
# print(filtered_data04)

filtered_data = pd.concat([filtered_data01, filtered_data02, filtered_data03, filtered_data04])

# 输出结果
print(filtered_data)

# 保存结果
filtered_data.to_csv('filtered_data.csv', index=False)






# 可以找一下在ZJ里面全是1|1，在其他个体里面没有1|1这种情况
zj_filtered03 = data[(zj_individuals == '1|1').all(axis=1)]
print(zj_filtered03.shape)
# print(zj_filtered03.head(10))
other_filtered03 = data[(other_individuals != '1|1').all(axis=1)]
print(other_filtered03.shape)
# 找到交集
filtered_data03 = pd.merge(zj_filtered03, other_filtered03, how='inner')
print(filtered_data03.shape)
# print(filtered_data03)

# 还可以找一下在ZJ里面是0｜0，在其他个体里面没有0|0的
zj_filtered04 = data[(zj_individuals == '0|0').all(axis=1)]
print(zj_filtered04.shape)
other_filtered04 = data[(other_individuals != '0|0').all(axis=1)]
print(other_filtered04.shape)
# 找到交集
filtered_data04 = pd.merge(zj_filtered04, other_filtered04, how='inner')
print(filtered_data04.shape)
# print(filtered_data04)

filtered_data = pd.concat([filtered_data03, filtered_data04])
# 保存结果
filtered_data.to_csv('filtered_data.csv', index=False)
