# 读取CSV文件
input_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取文件内容
with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 处理文件内容
lines = content.strip().split('\n')

# 确保表头正确
header = 'id,dimension,type,typeName,title,options,correct,analysis'

# 处理数据行
other_lines = []
scenario_lines = []

for line in lines[1:]:  # 跳过第一行
    if line.strip():
        # 手动解析行，处理列合并问题
        # 先按引号分割
        parts = line.split('"')
        
        # 提取第一个引号内的内容（包含id, dimension, type, typeName）
        first_part = parts[1] if len(parts) > 1 else ''
        first_fields = first_part.split(',')
        
        # 提取剩余部分
        remaining = ','.join(parts[2:]) if len(parts) > 2 else ''
        
        # 分割剩余部分为title, options, correct, analysis
        remaining_fields = remaining.split(',')
        
        # 构建正确的字段
        id_field = first_fields[0] if len(first_fields) > 0 else ''
        dimension = first_fields[1] if len(first_fields) > 1 else ''
        type_field = first_fields[2] if len(first_fields) > 2 else ''
        typeName = first_fields[3] if len(first_fields) > 3 else ''
        
        # 处理剩余字段
        title = ''
        options = ''
        correct = ''
        analysis = ''
        
        if len(remaining_fields) > 0:
            title = remaining_fields[0].strip()
        if len(remaining_fields) > 1:
            options = remaining_fields[1].strip()
        if len(remaining_fields) > 2:
            correct = remaining_fields[2].strip()
        if len(remaining_fields) > 3:
            analysis = ','.join(remaining_fields[3:]).strip()
        
        # 重新构建行
        new_row = [id_field, dimension, type_field, typeName, title, options, correct, analysis]
        
        # 检查是否是情景式问答
        if type_field == 'scenario':
            scenario_lines.append(new_row)
        else:
            other_lines.append(new_row)

# 重新组织文件：先放其他题目，再放情景式问答
processed_lines = [header]

# 添加其他题目
for row in other_lines:
    # 格式化行
    formatted_row = []
    for field in row:
        if ',' in field or '"' in field:
            field = field.replace('"', '""')
            field = f'"{field}"'
        formatted_row.append(field)
    processed_lines.append(','.join(formatted_row))

# 添加情景式问答题目
for row in scenario_lines:
    # 格式化行
    formatted_row = []
    for field in row:
        if ',' in field or '"' in field:
            field = field.replace('"', '""')
            field = f'"{field}"'
        formatted_row.append(field)
    processed_lines.append(','.join(formatted_row))

# 写回文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(processed_lines))

print(f"CSV文件格式已修复，共处理 {len(other_lines) + len(scenario_lines)} 行数据。")
print(f"其他题目数量: {len(other_lines)}")
print(f"情景式问答题目数量: {len(scenario_lines)}")
