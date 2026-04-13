# 读取CSV文件
input_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'
output_file = 'd:\\WorkBuddy\\LuojiStudio\\working\\ongoing\\aiedu-plus\\data\\ai-quiz-data.csv'

# 读取文件内容
with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# 处理文件内容
processed_lines = []

# 确保表头正确
header = 'id,dimension,type,typeName,title,options,correct,analysis'
processed_lines.append(header + '\n')

# 处理数据行
for line in lines[1:]:  # 跳过第一行
    if line.strip():
        # 简单处理：按逗号分割，但要处理引号内的逗号
        parts = []
        current = ''
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(current.strip())
                current = ''
            else:
                current += char
        
        if current:
            parts.append(current.strip())
        
        # 确保有8列
        while len(parts) < 8:
            parts.append('')
        
        # 重新组合为CSV行，确保格式正确
        new_line = []
        for part in parts:
            # 如果包含逗号或引号，用引号包围
            if ',' in part or '"' in part or '\n' in part:
                # 替换双引号为两个双引号
                part = part.replace('"', '""')
                # 用双引号包围
                part = f'"{part}"'
            new_line.append(part)
        
        processed_lines.append(','.join(new_line) + '\n')

# 写回文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(processed_lines)

print(f"CSV文件格式已修复，共处理 {len(processed_lines)-1} 行数据。")
