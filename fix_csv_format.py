import csv

# 读取CSV文件
input_file = 'D:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'D:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取CSV文件内容，处理换行问题
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 处理内容，确保每个题目都在一行中
# 查找情景式问答的开始和结束
lines = content.split('\n')
fixed_lines = []
current_line = ''

for line in lines:
    # 检查是否是新题目的开始（包含数字和逗号）
    if line.strip() and (line[0].isdigit() or (len(line) > 1 and line[0] == '"' and line[1].isdigit())):
        # 如果当前行不为空，添加到fixed_lines
        if current_line:
            fixed_lines.append(current_line)
        # 开始新行
        current_line = line
    else:
        # 否则，将当前行添加到current_line
        if current_line:
            current_line += ' ' + line.strip()

# 添加最后一行
if current_line:
    fixed_lines.append(current_line)

# 写回CSV文件
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print("已修复CSV文件格式")
