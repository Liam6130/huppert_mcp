#!/usr/bin/env python3
"""
NIRS-Toolbox MCP Server

功能：为AnalyzIR NIRS Toolbox提供MCP接口
作者：Liam
日期：2026-01-27
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from mcp.server.fastmcp import FastMCP

# ==========================================
# 1. 配置
# ==========================================

mcp = FastMCP("huppert", json_response=True)

# 工具箱路径 - 支持环境变量配置
NIRS_TOOLBOX_PATH = os.getenv("NIRS_TOOLBOX_PATH")

if NIRS_TOOLBOX_PATH is None:
    # 回退到默认路径（如果存在）
    default_path = Path("/Users/liam/Desktop/好用的工具/nirs-toolbox").expanduser()
    if default_path.exists():
        NIRS_TOOLBOX_PATH = default_path
        print(f"⚠️  使用默认路径：{NIRS_TOOLBOX_PATH}", file=sys.stderr)
    else:
        print(f"❌ 错误：请设置 NIRS_TOOLBOX_PATH 环境变量", file=sys.stderr)
        print(f"   示例: export NIRS_TOOLBOX_PATH=/path/to/nirs-toolbox", file=sys.stderr)
        sys.exit(1)
else:
    NIRS_TOOLBOX_PATH = Path(NIRS_TOOLBOX_PATH).expanduser()

if not NIRS_TOOLBOX_PATH.exists():
    print(f"❌ 错误：工具箱路径不存在: {NIRS_TOOLBOX_PATH}", file=sys.stderr)
    sys.exit(1)

print(f"✅ 工具箱路径：{NIRS_TOOLBOX_PATH}", file=sys.stderr)

# 定义命名空间路径
NIRS_NS = NIRS_TOOLBOX_PATH / "+nirs"
DEMOS_PATH = NIRS_TOOLBOX_PATH / "demos"

# ==========================================
# 2. 辅助函数
# ==========================================

def parse_matlab_class(filepath: Path) -> Dict:
    """解析MATLAB类文件 - 增强版"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    info = {
        'name': filepath.stem,
        'type': 'class',
        'description': '',
        'properties': [],
        'properties_detailed': [],  # 新增：详细属性信息
        'methods': [],
        'methods_detailed': [],  # 新增：详细方法信息
        'parent_class': '',
        'full_code': content,
        'file_path': str(filepath)
    }
    
    lines = content.split('\n')
    
    # 提取类定义
    class_match = re.search(r'classdef\s+(\w+)\s*(<\s*([\w.]+))?', content)
    if class_match:
        info['name'] = class_match.group(1)
        if class_match.group(3):
            info['parent_class'] = class_match.group(3)
    
    # 提取类注释（%% 开头的注释）
    comment_lines = []
    for i, line in enumerate(lines[1:20]):  # 在前20行找注释
        stripped = line.strip()
        if stripped.startswith('%%') or stripped.startswith('%'):
            comment_lines.append(stripped.lstrip('%').strip())
        elif comment_lines and not stripped.startswith('%'):
            break
    
    info['description'] = '\n'.join(comment_lines)
    
    # 提取属性（增强版 - 包含默认值和注释）
    props_match = re.search(r'properties(.*?)end', content, re.DOTALL)
    if props_match:
        props_text = props_match.group(1)
        for line in props_text.split('\n'):
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith('%'):
                info['properties'].append(line_stripped)
                
                # 解析属性详情
                prop_detail = parse_property_line(line_stripped)
                if prop_detail:
                    info['properties_detailed'].append(prop_detail)
    
    # 提取方法（增强版 - 包含签名和注释）
    method_pattern = r'function\s+(.*?)\s*=\s*(\w+)\s*\((.*?)\)|function\s+(\w+)\s*\((.*?)\)'
    for match in re.finditer(method_pattern, content):
        if match.group(2):  # 有返回值的函数
            method_name = match.group(2)
            return_vals = match.group(1)
            params = match.group(3)
        else:  # 无返回值的函数
            method_name = match.group(4)
            return_vals = ''
            params = match.group(5)
        
        if method_name and method_name != info['name']:
            info['methods'].append(method_name)
            
            # 提取方法注释
            method_comment = extract_method_comment(content, method_name)
            
            info['methods_detailed'].append({
                'name': method_name,
                'returns': return_vals,
                'params': params,
                'comment': method_comment
            })
    
    return info


def parse_property_line(line: str) -> Dict:
    """解析属性行，提取名称、默认值和注释"""
    # 移除行内注释
    if '%' in line:
        code_part = line.split('%')[0].strip()
        comment_part = line.split('%')[1].strip()
    else:
        code_part = line.strip()
        comment_part = ''
    
    # 解析属性名和默认值
    if '=' in code_part:
        parts = code_part.split('=')
        prop_name = parts[0].strip()
        default_value = parts[1].strip().rstrip(';')
    else:
        prop_name = code_part.rstrip(';').strip()
        default_value = ''
    
    return {
        'name': prop_name,
        'default': default_value,
        'comment': comment_part
    }


def extract_method_comment(content: str, method_name: str) -> str:
    """提取方法的注释说明"""
    # 查找方法定义位置
    pattern = f'function\\s+.*?{method_name}\\s*\\('
    match = re.search(pattern, content)
    if not match:
        return ''
    
    # 提取方法后的注释
    start_pos = match.end()
    lines_after = content[start_pos:].split('\n')
    
    comments = []
    for line in lines_after[:10]:  # 只看后面10行
        stripped = line.strip()
        if stripped.startswith('%'):
            comments.append(stripped.lstrip('%').strip())
        elif comments and not stripped.startswith('%'):
            break
    
    return '\n'.join(comments)


def parse_matlab_function(filepath: Path) -> Dict:
    """解析MATLAB函数文件"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    info = {
        'name': filepath.stem,
        'type': 'function',
        'description': '',
        'signature': '',
        'full_code': content
    }
    
    lines = content.split('\n')
    
    # 提取函数签名
    for line in lines[:20]:
        if line.strip().startswith('function'):
            info['signature'] = line.strip()
            break
    
    # 提取注释
    comment_lines = []
    in_comment = False
    for i, line in enumerate(lines[:50]):
        stripped = line.strip()
        if i == 0 and stripped.startswith('function'):
            in_comment = True
            continue
        if in_comment and stripped.startswith('%'):
            comment_lines.append(stripped.lstrip('%').strip())
        elif in_comment and not stripped.startswith('%'):
            break
    
    info['description'] = '\n'.join(comment_lines)
    
    return info


def get_namespace_files(namespace_path: Path) -> Dict[str, List[Path]]:
    """获取命名空间下的所有文件，按子命名空间分类"""
    categories = {}
    
    for subdir in namespace_path.iterdir():
        if not subdir.is_dir():
            continue
        
        # 跳过非命名空间目录
        if not subdir.name.startswith('+'):
            continue
        
        category_name = subdir.name[1:]  # 去掉 + 前缀
        m_files = list(subdir.rglob('*.m'))
        categories[category_name] = m_files
    
    return categories


def format_module_info(info: Dict, namespace: str) -> str:
    """格式化模块信息为markdown"""
    output = f"# 📦 {info['name']}\n\n"
    
    if info['type'] == 'class':
        output += f"**类型**: MATLAB 类\n"
        if info['parent_class']:
            output += f"**继承自**: `{info['parent_class']}`\n"
        output += "\n"
        
        if info['description']:
            output += f"## 📄 说明\n\n{info['description']}\n\n"
        
        if info['properties']:
            output += f"## ⚙️ 属性\n\n"
            for prop in info['properties']:
                output += f"- `{prop}`\n"
            output += "\n"
        
        if info['methods']:
            output += f"## 🔧 方法\n\n"
            for method in info['methods'][:10]:  # 只显示前10个
                output += f"- `{method}()`\n"
            if len(info['methods']) > 10:
                output += f"- ... 还有 {len(info['methods']) - 10} 个方法\n"
            output += "\n"
        
        output += f"## 💻 使用方式\n\n"
        output += f"```matlab\n"
        output += f"% 创建实例\n"
        output += f"obj = nirs.{namespace}.{info['name']}();\n"
        output += f"```\n\n"
    
    else:  # function
        if info['signature']:
            output += f"## 函数签名\n\n```matlab\n{info['signature']}\n```\n\n"
        
        if info['description']:
            output += f"## 📄 说明\n\n{info['description']}\n\n"
        
        output += f"## 💻 使用方式\n\n"
        output += f"```matlab\n"
        output += f"result = nirs.{namespace}.{info['name']}(...);\n"
        output += f"```\n\n"
    
    output += f"## 📝 完整代码\n\n"
    output += f"```matlab\n{info['full_code']}\n```\n\n"
    
    return output


# ==========================================
# 3. Resources: 暴露工具箱内容
# ==========================================

@mcp.resource("list://categories")
def list_categories() -> str:
    """列出所有命名空间类别"""
    categories = get_namespace_files(NIRS_NS)
    
    output = "# 🧠 NIRS-Toolbox 模块分类\n\n"
    output += f"工具箱共包含 **{len(categories)}** 个主要类别：\n\n"
    
    # 按文件数量排序
    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    
    for cat_name, files in sorted_cats:
        output += f"## {cat_name} ({len(files)} 个文件)\n"
        output += f"- 查看详情：`category://{cat_name}`\n\n"
    
    output += "\n---\n"
    output += "💡 使用方式：\n"
    output += "- 查看某个类别：`category://类别名`\n"
    output += "- 查看模块详情：`module://类别名/模块名`\n"
    
    return output


@mcp.resource("category://{category}")
def get_category(category: str) -> str:
    """获取指定类别的所有模块"""
    category_path = NIRS_NS / f"+{category}"
    
    if not category_path.exists():
        available = [d.name[1:] for d in NIRS_NS.iterdir() if d.is_dir() and d.name.startswith('+')]
        return f"""
❌ 类别 '{category}' 不存在

📁 可用类别：
{chr(10).join([f"  - {cat}" for cat in sorted(available)])}

💡 使用方式：category://类别名
"""
    
    output = f"# 📂 nirs.{category}\n\n"
    
    # 列出所有.m文件
    m_files = sorted(category_path.glob('*.m'))
    
    if not m_files:
        # 可能是包含子目录的类别
        subdirs = [d for d in category_path.iterdir() if d.is_dir()]
        if subdirs:
            output += "## 子模块\n\n"
            for subdir in sorted(subdirs):
                subfiles = list(subdir.glob('*.m'))
                output += f"### {subdir.name} ({len(subfiles)} 个文件)\n"
                for f in sorted(subfiles)[:5]:
                    output += f"- `{f.stem}` - `module://{category}/{f.stem}`\n"
                if len(subfiles) > 5:
                    output += f"- ... 还有 {len(subfiles) - 5} 个文件\n"
                output += "\n"
        else:
            output += "（该类别下无.m文件）\n"
    else:
        output += f"共 **{len(m_files)}** 个模块/函数：\n\n"
        
        for mfile in m_files:
            # 快速提取第一行注释
            with open(mfile, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                first_comment = ""
                for line in lines[1:10]:
                    if line.strip().startswith('%'):
                        first_comment = line.strip().lstrip('%').strip()
                        break
            
            output += f"### {mfile.stem}\n"
            if first_comment:
                output += f"{first_comment}\n"
            output += f"- 查看详情：`module://{category}/{mfile.stem}`\n\n"
    
    return output


@mcp.resource("module://{category}/{name}")
def get_module(category: str, name: str) -> str:
    """获取指定模块的详细信息"""
    # 尝试在类别目录下查找
    module_path = NIRS_NS / f"+{category}" / f"{name}.m"
    
    if not module_path.exists():
        # 尝试在子目录中查找
        category_path = NIRS_NS / f"+{category}"
        found_files = list(category_path.rglob(f"{name}.m"))
        if found_files:
            module_path = found_files[0]
        else:
            return f"❌ 模块 '{category}/{name}' 不存在"
    
    # 判断是类还是函数
    with open(module_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline()
    
    if 'classdef' in first_line:
        info = parse_matlab_class(module_path)
    else:
        info = parse_matlab_function(module_path)
    
    return format_module_info(info, category)


@mcp.resource("demo://{demo_name}")
def get_demo(demo_name: str) -> str:
    """获取示例脚本"""
    demo_path = DEMOS_PATH / f"{demo_name}.m"
    
    if not demo_path.exists():
        # 列出可用demo
        available = [f.stem for f in DEMOS_PATH.glob('*.m')]
        return f"""
❌ 示例 '{demo_name}' 不存在

📁 可用示例：
{chr(10).join([f"  - {demo}" for demo in sorted(available)])}

💡 使用方式：demo://示例名
"""
    
    with open(demo_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    output = f"# 💡 {demo_name}\n\n"
    output += "## 完整代码\n\n"
    output += f"```matlab\n{code}\n```\n\n"
    output += "---\n"
    output += f"📍 文件路径：{demo_path}\n"
    output += f"📊 代码行数：{len(code.splitlines())} 行\n"
    
    return output


@mcp.resource("list://demos")
def list_demos() -> str:
    """列出所有示例"""
    demo_files = sorted(DEMOS_PATH.glob('*.m'))
    
    output = "# 💡 NIRS-Toolbox 示例脚本\n\n"
    output += f"共 **{len(demo_files)}** 个示例：\n\n"
    
    for demo_file in demo_files:
        with open(demo_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            # 提取第一行注释
            first_comment = ""
            for line in lines[:10]:
                if line.strip().startswith('%'):
                    first_comment = line.strip().lstrip('%').strip()
                    break
        
        output += f"### {demo_file.stem}\n"
        if first_comment:
            output += f"{first_comment}\n"
        output += f"- 查看代码：`demo://{demo_file.stem}`\n\n"
    
    return output


# ==========================================
# 4. Tools: 搜索和查询功能
# ==========================================

@mcp.tool()
def search_module(keyword: str) -> str:
    """
    搜索包含关键词的模块
    
    Args:
        keyword: 搜索关键词（如 "filter", "glm", "connectivity"）
    
    Returns:
        匹配的模块列表
    """
    categories = get_namespace_files(NIRS_NS)
    results = []
    
    for cat_name, files in categories.items():
        for mfile in files:
            with open(mfile, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 搜索关键词（不区分大小写）
            if keyword.lower() in content.lower() or keyword.lower() in mfile.stem.lower():
                # 提取简介
                lines = content.split('\n')
                description = ""
                for line in lines[1:10]:
                    if line.strip().startswith('%'):
                        description = line.strip().lstrip('%').strip()
                        break
                
                results.append({
                    'name': mfile.stem,
                    'category': cat_name,
                    'description': description,
                    'path': f"module://{cat_name}/{mfile.stem}"
                })
    
    if not results:
        return f"❌ 未找到包含 '{keyword}' 的模块"
    
    output = f"# 🔍 搜索结果：'{keyword}'\n\n"
    output += f"找到 **{len(results)}** 个匹配的模块：\n\n"
    
    # 按类别分组
    by_category = {}
    for r in results:
        if r['category'] not in by_category:
            by_category[r['category']] = []
        by_category[r['category']].append(r)
    
    for cat, items in sorted(by_category.items()):
        output += f"## nirs.{cat}\n\n"
        for item in items[:10]:  # 每个类别最多显示10个
            output += f"### {item['name']}\n"
            if item['description']:
                output += f"{item['description']}\n"
            output += f"- 查看详情：`{item['path']}`\n\n"
    
    return output


@mcp.tool()
def find_workflow(task: str) -> str:
    """
    查找适合特定任务的工作流
    
    Args:
        task: 任务描述（如 "preprocessing", "glm analysis", "connectivity"）
    
    Returns:
        推荐的模块和工作流
    """
    # 定义常见工作流
    workflows = {
        'preprocessing': {
            'description': 'fNIRS数据预处理流程',
            'modules': [
                ('modules', 'BandPassFilter', '带通滤波'),
                ('modules', 'OpticalDensity', '转换为光密度'),
                ('modules', 'BeerLambertLaw', '转换为HbO/HbR'),
                ('modules', 'AR_IRLS', 'AR-IRLS统计分析'),
            ]
        },
        'glm': {
            'description': 'GLM一般线性模型分析',
            'modules': [
                ('modules', 'OpticalDensity', '转换为光密度'),
                ('modules', 'BeerLambertLaw', '转换为HbO/HbR'),
                ('modules', 'AR_IRLS', 'AR-IRLS回归'),
                ('modules', 'MixedEffects', '混合效应模型（组分析）'),
            ]
        },
        'connectivity': {
            'description': '功能连接性分析',
            'modules': [
                ('modules', 'BandPassFilter', '带通滤波（0.01-0.1Hz）'),
                ('modules', 'OpticalDensity', '转换为光密度'),
                ('modules', 'BeerLambertLaw', '转换为HbO/HbR'),
                ('modules', 'Connectivity', '计算功能连接'),
            ]
        },
        'image_reconstruction': {
            'description': '图像重建/源定位',
            'modules': [
                ('modules', 'OpticalDensity', '转换为光密度'),
                ('registration', 'Register', '配准到标准空间'),
                ('modules', 'ImageReconMFX', 'MFX图像重建'),
            ]
        }
    }
    
    # 查找匹配的工作流
    task_lower = task.lower()
    matched = None
    for key, workflow in workflows.items():
        if key in task_lower or any(keyword in task_lower for keyword in key.split('_')):
            matched = workflow
            break
    
    if not matched:
        return f"""
❌ 未找到匹配 '{task}' 的工作流

💡 可用的工作流关键词：
- preprocessing - 预处理
- glm - GLM统计分析
- connectivity - 功能连接
- image_reconstruction - 图像重建

请尝试使用这些关键词搜索。
"""
    
    output = f"# 🔄 工作流：{matched['description']}\n\n"
    output += "## 推荐的处理流程\n\n"
    
    for i, (cat, module, desc) in enumerate(matched['modules'], 1):
        output += f"{i}. **{module}** - {desc}\n"
        output += f"   - 查看详情：`module://{cat}/{module}`\n\n"
    
    output += "## 💻 示例代码\n\n"
    output += "```matlab\n"
    output += "% 创建处理流水线\n"
    for cat, module, _ in matched['modules']:
        output += f"job = nirs.{cat}.{module}(job);\n"
    output += "\n% 运行流水线\n"
    output += "data = job.run(raw_data);\n"
    output += "```\n"
    
    return output


@mcp.tool()
def get_module_details(module_name: str, include_source: bool = False) -> str:
    """
    获取模块的完整详细信息
    
    Args:
        module_name: 模块名（如 BandPassFilter）
        include_source: 是否包含完整源代码（默认 False）
    
    Returns:
        模块的完整文档，包括属性、方法、使用示例
    """
    # 在所有类别中搜索模块
    categories = get_namespace_files(NIRS_NS)
    
    module_path = None
    category = None
    
    for cat_name, files in categories.items():
        for mfile in files:
            if mfile.stem == module_name:
                module_path = mfile
                category = cat_name
                break
        if module_path:
            break
    
    if not module_path:
        return f"❌ 模块 '{module_name}' 不存在。使用 search_module() 搜索模块。"
    
    # 判断是类还是函数
    with open(module_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline()
        content = f.read()
        full_content = first_line + content
    
    if 'classdef' in first_line:
        info = parse_matlab_class(module_path)
        return format_class_details(info, category, include_source)
    else:
        info = parse_matlab_function(module_path)
        return format_function_details(info, category, include_source)


def format_class_details(info: Dict, category: str, include_source: bool) -> str:
    """格式化类的详细信息"""
    output = f"# 📦 nirs.{category}.{info['name']}\n\n"
    
    # 基本信息
    output += f"**类型**: MATLAB 类\n"
    if info['parent_class']:
        output += f"**继承自**: `{info['parent_class']}`\n"
    output += f"**路径**: `{info.get('file_path', 'N/A')}`\n\n"
    
    # 描述
    if info['description']:
        output += f"## 📄 描述\n\n{info['description']}\n\n"
    
    # Properties 详细表格
    if info.get('properties_detailed'):
        output += f"## ⚙️ Properties (属性)\n\n"
        output += "| 属性名 | 默认值 | 说明 |\n"
        output += "|--------|--------|------|\n"
        
        for prop in info['properties_detailed']:
            name = prop['name']
            default = prop['default'] if prop['default'] else '(无默认值)'
            comment = prop['comment'] if prop['comment'] else '-'
            output += f"| `{name}` | `{default}` | {comment} |\n"
        output += "\n"
    elif info.get('properties'):
        # 备用方案：简单列表
        output += f"## ⚙️ Properties (属性)\n\n"
        for prop in info['properties']:
            output += f"- `{prop}`\n"
        output += "\n"
    
    # Methods
    if info.get('methods_detailed'):
        output += f"## 🔧 Methods (方法)\n\n"
        for method in info['methods_detailed'][:5]:  # 只显示前5个主要方法
            output += f"### `{method['name']}({method.get('params', '')})`\n"
            if method.get('returns'):
                output += f"**返回**: `{method['returns']}`\n"
            if method.get('comment'):
                output += f"{method['comment']}\n"
            output += "\n"
        
        if len(info['methods_detailed']) > 5:
            output += f"*... 还有 {len(info['methods_detailed']) - 5} 个方法*\n\n"
    elif info.get('methods'):
        output += f"## 🔧 Methods (方法)\n\n"
        for method in info['methods'][:10]:
            output += f"- `{method}()`\n"
        if len(info['methods']) > 10:
            output += f"- ... 还有 {len(info['methods']) - 10} 个方法\n"
        output += "\n"
    
    # 使用示例
    output += f"## 💻 基本使用\n\n"
    output += f"### 创建实例\n"
    output += f"```matlab\n"
    output += f"% 独立使用\n"
    output += f"job = nirs.{category}.{info['name']}();\n"
    
    # 根据常见模块添加参数示例
    if info['properties_detailed']:
        output += f"\n% 设置参数\n"
        for prop in info['properties_detailed'][:3]:  # 显示前3个属性
            if prop['default']:
                output += f"job.{prop['name']} = {prop['default']};  % {prop['comment']}\n"
    
    output += f"\n% 运行\n"
    output += f"result = job.run(data);\n"
    output += f"```\n\n"
    
    # 流水线使用
    output += f"### 在流水线中使用\n"
    output += f"```matlab\n"
    output += f"% 创建流水线\n"
    output += f"job1 = nirs.{category}.{info['name']}();\n"
    output += f"job2 = nirs.modules.NextModule(job1);  % 链式连接\n"
    output += f"\n% 运行流水线\n"
    output += f"result = job2.run(data);\n"
    output += f"```\n\n"
    
    # 相关模块推荐
    output += f"## 🔗 相关模块\n\n"
    related = suggest_related_modules(info['name'], category)
    if related:
        for rel in related:
            output += f"- `{rel['name']}` - {rel['description']}\n"
    else:
        output += f"*使用 `search_module()` 查找相关模块*\n"
    output += "\n"
    
    # 完整源代码（可选）
    if include_source:
        output += f"## 📝 完整源代码\n\n"
        output += f"```matlab\n{info['full_code']}\n```\n\n"
    else:
        output += f"## 📝 源代码\n\n"
        output += f"*使用 `get_module_details(\"{info['name']}\", include_source=True)` 查看完整源代码*\n\n"
    
    # 提示
    output += f"## 💡 提示\n\n"
    output += f"- 查看官方demo: `demo://fnirs_analysis_demo`\n"
    output += f"- 对比其他模块: `compare_modules(\"{info['name']}\", \"OtherModule\")`\n"
    output += f"- 搜索相似功能: `search_module(\"关键词\")`\n"
    
    return output


def format_function_details(info: Dict, category: str, include_source: bool) -> str:
    """格式化函数的详细信息"""
    output = f"# 🔧 nirs.{category}.{info['name']}\n\n"
    
    # 基本信息
    output += f"**类型**: MATLAB 函数\n"
    output += f"**路径**: `{info.get('file_path', 'N/A')}`\n\n"
    
    # 函数签名
    if info.get('signature'):
        output += f"## 📝 函数签名\n\n"
        output += f"```matlab\n{info['signature']}\n```\n\n"
    
    # 描述
    if info['description']:
        output += f"## 📄 说明\n\n{info['description']}\n\n"
    
    # 使用示例
    output += f"## 💻 使用方式\n\n"
    output += f"```matlab\n"
    output += f"result = nirs.{category}.{info['name']}(...);\n"
    output += f"```\n\n"
    
    # 完整源代码
    if include_source:
        output += f"## 📝 完整源代码\n\n"
        output += f"```matlab\n{info['full_code']}\n```\n\n"
    
    return output


def suggest_related_modules(module_name: str, category: str) -> List[Dict]:
    """根据模块名推荐相关模块"""
    # 预定义的相关模块映射
    related_map = {
        'BandPassFilter': [
            {'name': 'WaveletFilter', 'description': '小波滤波（适合运动伪迹）'},
            {'name': 'BaselinePCAFilter', 'description': 'PCA基线滤波'},
            {'name': 'OpticalDensity', 'description': '光密度转换（滤波前必需）'},
        ],
        'OpticalDensity': [
            {'name': 'BandPassFilter', 'description': '带通滤波（下一步）'},
            {'name': 'BeerLambertLaw', 'description': 'Beer-Lambert转换'},
        ],
        'BeerLambertLaw': [
            {'name': 'OpticalDensity', 'description': '光密度转换（前一步）'},
            {'name': 'AR_IRLS', 'description': 'GLM统计分析（下一步）'},
        ],
        'AR_IRLS': [
            {'name': 'MixedEffects', 'description': '组水平分析'},
            {'name': 'GLM', 'description': 'GLM模型'},
        ],
        'WaveletFilter': [
            {'name': 'BandPassFilter', 'description': '带通滤波'},
            {'name': 'TDDR', 'description': '时域导数分布修正'},
        ],
    }
    
    return related_map.get(module_name, [])


@mcp.tool()
def compare_modules(name1: str, name2: str) -> str:
    """
    对比两个模块
    
    Args:
        name1: 第一个模块名
        name2: 第二个模块名
    
    Returns:
        两个模块的对比分析
    """
    # 在所有类别中搜索
    categories = get_namespace_files(NIRS_NS)
    
    module1_path = None
    module2_path = None
    cat1 = None
    cat2 = None
    
    for cat_name, files in categories.items():
        for mfile in files:
            if mfile.stem == name1:
                module1_path = mfile
                cat1 = cat_name
            if mfile.stem == name2:
                module2_path = mfile
                cat2 = cat_name
    
    if not module1_path:
        return f"❌ 模块 '{name1}' 不存在"
    if not module2_path:
        return f"❌ 模块 '{name2}' 不存在"
    
    # 解析两个模块
    with open(module1_path, 'r', encoding='utf-8', errors='ignore') as f:
        code1 = f.read()
    with open(module2_path, 'r', encoding='utf-8', errors='ignore') as f:
        code2 = f.read()
    
    output = f"# 🔄 模块对比：{name1} vs {name2}\n\n"
    output += f"## 模块 1: nirs.{cat1}.{name1}\n\n"
    output += f"```matlab\n{code1[:500]}...\n```\n\n"
    output += f"## 模块 2: nirs.{cat2}.{name2}\n\n"
    output += f"```matlab\n{code2[:500]}...\n```\n\n"
    output += "## 💡 请AI分析\n\n"
    output += "请帮我对比这两个模块的：\n"
    output += "1. 功能差异\n"
    output += "2. 适用场景\n"
    output += "3. 参数设置\n"
    output += "4. 优缺点\n"
    output += "5. 使用建议\n"
    
    return output


# ==========================================
# 5. Prompts: 常见问题模板
# ==========================================

@mcp.prompt()
def how_to_preprocess() -> str:
    """fNIRS数据预处理指南"""
    return """
我想对fNIRS数据进行预处理，请帮我：

1. 查看 `find_workflow("preprocessing")` 获取推荐流程
2. 解释每个步骤的作用
3. 说明参数如何设置
4. 提供完整的MATLAB代码示例

【我的数据】
- 设备类型：[NIRx/Hitachi/其他]
- 采样率：[Hz]
- 通道数：[数量]
- 任务类型：[block design/event-related]
"""


@mcp.prompt()
def how_to_glm_analysis() -> str:
    """GLM统计分析指南"""
    return """
我想进行GLM统计分析，请帮我：

1. 查看 `module://modules/AR_IRLS` 了解AR-IRLS模型
2. 查看 `demo://fnirs_analysis_demo` 了解完整流程
3. 解释设计矩阵的构建
4. 说明如何解释统计结果
5. 提供完整代码示例

【我的实验设计】
- 任务类型：[描述]
- 刺激时长：[秒]
- 间隔时长：[秒]
- 重复次数：[次数]
"""


@mcp.prompt()
def how_to_load_data(device: str = "NIRx") -> str:
    """数据加载指南"""
    return f"""
我想加载 {device} 设备的fNIRS数据，请帮我：

1. 查看 `category://io` 找到对应的加载函数
2. 查看 `module://io/load{device}` 的详细用法
3. 解释数据格式要求
4. 提供加载代码示例
5. 说明常见问题和解决方法

【我的数据】
- 数据格式：{device}
- 文件路径：[填写]
- 是否包含探头信息：[是/否]
"""


@mcp.prompt()
def build_pipeline(task: str = "group analysis") -> str:
    """构建完整分析流水线"""
    return f"""
我想构建一个完整的fNIRS分析流水线，用于：{task}

请帮我：

1. 查看相关的demo示例
2. 列出需要的所有模块
3. 解释每个模块的作用和参数设置
4. 构建完整的流水线代码
5. 说明结果解释和可视化

【分析目标】
- 任务：{task}
- 受试者数量：[填写]
- 数据来源：[填写]
- 期望输出：[填写]
"""


# ==========================================
# 6. 运行服务器
# ==========================================

if __name__ == "__main__":
    print("="*70, file=sys.stderr)
    print("🧠 NIRS-Toolbox MCP Server", file=sys.stderr)
    print("="*70, file=sys.stderr)
    print(f"📁 工具箱路径: {NIRS_TOOLBOX_PATH}", file=sys.stderr)
    print(f"📊 命名空间: {NIRS_NS}", file=sys.stderr)
    print(f"💡 示例目录: {DEMOS_PATH}", file=sys.stderr)
    print(f"✅ 服务器已启动", file=sys.stderr)
    print("="*70, file=sys.stderr)
    
    mcp.run(transport="stdio")
