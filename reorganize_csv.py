import csv

# 读取CSV文件
input_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 尝试不同的编码格式
encodings = ['utf-8', 'gbk', 'utf-16', 'ansi']
rows = []

for encoding in encodings:
    try:
        with open(input_file, 'r', encoding=encoding, errors='ignore') as f:
            reader = csv.reader(f)
            rows = list(reader)
        print(f"成功使用编码 {encoding} 读取文件")
        break
    except Exception as e:
        print(f"尝试编码 {encoding} 失败: {e}")

if not rows:
    print("无法读取文件，使用默认方式")
    with open(input_file, 'r', errors='ignore') as f:
        content = f.read()
    rows = [line.split(',') for line in content.split('\n') if line.strip()]

header = rows[0]
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

print(f"CSV文件已重新组织，情景式问答题目已移到文件末尾。")
print(f"处理前总行数: {len(rows)}")
print(f"处理后总行数: {len(new_rows)}")
print(f"情景式问答题目数量: {len(scenario_rows)}")
print(f"其他题目数量: {len(other_rows)}")
