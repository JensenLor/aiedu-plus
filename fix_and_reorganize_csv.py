import csv

# 读取CSV文件
input_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取文件内容
with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 处理文件内容，修复格式
lines = content.strip().split('\n')

# 确保第一行是表头
header = ['id', 'dimension', 'type', 'typeName', 'title', 'options', 'correct', 'analysis']

# 处理数据行
rows = [header]
for line in lines[1:]:  # 跳过第一行（可能是表头或错误的行）
    if line.strip():
        # 尝试分割行
        parts = line.split('?')
        if len(parts) >= 8:
            # 重组行数据
            row = [
                parts[0].strip(),  # id
                parts[1].strip(),  # dimension
                parts[2].strip(),  # type
                parts[3].strip(),  # typeName
                '?'.join(parts[4:-3]).strip(),  # title (可能包含?)
                parts[-3].strip(),  # options
                parts[-2].strip(),  # correct
                parts[-1].strip()   # analysis
            ]
            rows.append(row)

# 分离情景式问答题目和其他题目
scenario_rows = []
other_rows = []

for row in rows[1:]:
    if len(row) > 2 and 'scenario' in row[2]:
        scenario_rows.append(row)
    else:
        other_rows.append(row)

# 重新组织行：先放其他题目，再放情景式问答
new_rows = [header] + other_rows + scenario_rows

# 写回CSV文件
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"CSV文件已修复并重新组织，情景式问答题目已移到文件末尾。")
print(f"处理前总行数: {len(rows)}")
print(f"处理后总行数: {len(new_rows)}")
print(f"情景式问答题目数量: {len(scenario_rows)}")
print(f"其他题目数量: {len(other_rows)}")
