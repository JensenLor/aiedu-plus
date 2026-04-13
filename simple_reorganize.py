# 读取CSV文件内容
input_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取文件
with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# 分离表头和数据
header = lines[0]
data_lines = lines[1:]

# 分离情景式问答题目和其他题目
scenario_lines = []
other_lines = []

for line in data_lines:
    if 'scenario' in line:
        scenario_lines.append(line)
    else:
        other_lines.append(line)

# 重新组织文件：先放其他题目，再放情景式问答
new_content = header + ''.join(other_lines) + ''.join(scenario_lines)

# 写回文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"CSV文件已重新组织，情景式问答题目已移到文件末尾。")
print(f"总题目数: {len(data_lines)}")
print(f"情景式问答题目数量: {len(scenario_lines)}")
print(f"其他题目数量: {len(other_lines)}")
