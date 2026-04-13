import csv

# 读取CSV文件
input_file = 'D:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'D:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取CSV文件内容
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# 清理情景式问答的options字段
for i, row in enumerate(rows):
    if len(row) >= 4 and row[3] == '情景式问答':
        # 将options字段设置为空
        if len(row) >= 6:
            row[5] = ''

# 写回CSV文件
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("已清理情景式问答的options字段")
