# 🔬 MCP 近红外工具箱实现指南

**创建日期**：2026-01-27  
**目标**：为近红外分析工具箱创建 MCP Server，让 AI 可以直接查阅文档和代码

---

## 📑 目录

1. [背景与动机](#1-背景与动机)
2. [MCP 核心概念](#2-mcp-核心概念)
3. [系统设计](#3-系统设计)
4. [完整实现](#4-完整实现)
5. [配置部署](#5-配置部署)
6. [使用示例](#6-使用示例)
7. [进阶功能](#7-进阶功能)
8. [故障排查](#8-故障排查)

---

## 1. 背景与动机

### 1.1 现状问题

**你的工具箱：**
- ✅ 有完整的近红外分析工具箱（MATLAB）
- ✅ 包含预处理、建模、可视化等功能
- ✅ 有 .m 源代码文件

**遇到的问题：**
- ❌ 查看文档费时费力
- ❌ 阅读 .m 文件不直观
- ❌ 记不住每个函数的用法
- ❌ 需要在多个文件间切换

---

### 1.2 解决方案：MCP Server

**MCP (Model Context Protocol)** 可以让 AI 直接访问你的工具箱：

```
你的问题：
"怎么使用 SNV 标准化？"
    ↓
Claude Desktop (MCP Client)
    ↓
MCP Server (你的工具箱)
    ↓ 自动读取
function://preprocessing/snv
    ↓
AI 解释给你听
```

**效果：**
- ✅ AI 自动查阅文档和代码
- ✅ 你只需要提问
- ✅ 不需要手动翻文件
- ✅ AI 可以对比、解释、生成示例

---

## 2. MCP 核心概念

### 2.1 MCP 三大能力

#### 1. Resources（资源）📄

**定义：** 文件式的数据，AI 可以读取

**场景：**
```python
@mcp.resource("docs://preprocessing")
def get_preprocessing_docs():
    return "预处理文档内容..."

# AI 自动读取：docs://preprocessing
```

**适用：**
- ✅ 文档
- ✅ 代码文件
- ✅ 配置文件
- ✅ 数据字典

---

#### 2. Tools（工具）🔧

**定义：** AI 可以调用的函数

**场景：**
```python
@mcp.tool()
def search_function(keyword: str) -> str:
    """搜索包含关键词的函数"""
    # 搜索逻辑...
    return results

# AI 主动调用：search_function("smooth")
```

**适用：**
- ✅ 搜索功能
- ✅ 数据处理
- ✅ 计算分析
- ✅ 自动化任务

---

#### 3. Prompts（提示模板）💬

**定义：** 预设的问题模板

**场景：**
```python
@mcp.prompt()
def how_to_preprocess(method: str):
    return f"我想使用 {method} 预处理，请帮我..."

# 用户选择：how_to_preprocess("SNV")
```

**适用：**
- ✅ 常见问题
- ✅ 工作流模板
- ✅ 最佳实践

---

### 2.2 MCP 工作流程

```
┌──────────────────────────────────────────────────────────┐
│  你 (User)                                                │
│  "怎么使用 PLS 建模？"                                     │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                             │
│  - 接收你的问题                                           │
│  - 决定需要哪些资源                                       │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│  NIR Tools MCP Server                                    │
│  - 暴露文档：docs://analysis                              │
│  - 暴露代码：function://analysis/pls                      │
│  - 暴露示例：example://example_pls                        │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│  你的工具箱文件系统                                       │
│  ~/NIRTools/                                             │
│    ├── docs/analysis.md                                  │
│    ├── functions/analysis/pls.m                          │
│    └── examples/example_pls.m                            │
└──────────────────────────────────────────────────────────┘
```

---

## 3. 系统设计

### 3.1 工具箱结构假设

假设你的工具箱结构如下（如果不同，可以调整）：

```
NIRTools/
├── docs/                      # 文档目录
│   ├── preprocessing.md       # 预处理方法文档
│   ├── analysis.md            # 分析方法文档
│   ├── visualization.md       # 可视化方法文档
│   └── README.md              # 总览
│
├── functions/                 # 函数代码
│   ├── preprocessing/         # 预处理函数
│   │   ├── savgol.m           # Savitzky-Golay 平滑
│   │   ├── snv.m              # SNV 标准化
│   │   ├── msc.m              # MSC 多元散射校正
│   │   ├── sg.m               # SG 一阶导数
│   │   └── normalize.m        # 归一化
│   │
│   ├── analysis/              # 分析函数
│   │   ├── pls.m              # PLS 回归
│   │   ├── pcr.m              # PCR 主成分回归
│   │   ├── svm.m              # SVM 分类
│   │   ├── lda.m              # LDA 判别分析
│   │   └── ann.m              # 人工神经网络
│   │
│   └── visualization/         # 可视化函数
│       ├── plot_spectrum.m    # 绘制光谱
│       ├── plot_scores.m      # 绘制得分图
│       └── plot_loadings.m    # 绘制载荷图
│
├── examples/                  # 使用示例
│   ├── example_preprocess.m   # 预处理完整流程
│   ├── example_pls.m          # PLS 建模示例
│   ├── example_classification.m # 分类示例
│   └── example_visualization.m  # 可视化示例
│
└── README.md                  # 工具箱说明
```

---

### 3.2 MCP Server 架构

```
NIR Tools MCP Server
├── Resources (资源) - AI 可以读取
│   ├── docs://{doc_name}
│   │   └── 返回指定文档内容
│   │
│   ├── function://{category}/{func_name}
│   │   └── 返回函数源代码 + 注释提取
│   │
│   ├── example://{example_name}
│   │   └── 返回使用示例代码
│   │
│   └── list://functions
│       └── 列出所有可用函数
│
├── Tools (工具) - AI 可以主动调用
│   ├── search_function(keyword)
│   │   └── 搜索包含关键词的函数
│   │
│   └── explain_function(category, func_name)
│       └── 详细解释函数用法
│
└── Prompts (模板) - 预设问题
    ├── how_to_preprocess(method)
    │   └── "如何使用 XX 预处理？"
    │
    └── build_model(method, task)
        └── "如何用 XX 方法建模？"
```

---

## 4. 完整实现

### 4.1 创建 MCP Server

**文件：`nir_tools_server.py`**

```python
#!/usr/bin/env python3
"""
NIR Tools MCP Server

功能：
1. 暴露近红外分析工具箱的文档、代码和示例
2. 提供搜索和查询功能
3. 预设常见问题模板

作者：Liam
日期：2026-01-27
"""

import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# ==========================================
# 1. 配置区域
# ==========================================

# 初始化 MCP server
mcp = FastMCP("nir-tools", json_response=True)

# ⚠️ 修改为你的工具箱路径
NIR_TOOLS_PATH = Path("~/Desktop/NIRTools").expanduser()

# 确保路径存在
if not NIR_TOOLS_PATH.exists():
    print(f"❌ 错误：工具箱路径不存在: {NIR_TOOLS_PATH}", file=sys.stderr)
    print(f"   请修改 nir_tools_server.py 中的 NIR_TOOLS_PATH", file=sys.stderr)
    sys.exit(1)

print(f"✅ 工具箱路径：{NIR_TOOLS_PATH}", file=sys.stderr)

# ==========================================
# 2. Resources: 暴露工具箱内容
# ==========================================

@mcp.resource("docs://{doc_name}")
def get_documentation(doc_name: str) -> str:
    """
    获取工具箱文档
    
    可用文档：
    - preprocessing: 预处理方法文档
    - analysis: 分析方法文档
    - visualization: 可视化方法文档
    - README: 工具箱总览
    
    使用：docs://preprocessing
    """
    docs_path = NIR_TOOLS_PATH / "docs" / f"{doc_name}.md"
    
    # 如果没有 .md 后缀，尝试其他格式
    if not docs_path.exists():
        docs_path = NIR_TOOLS_PATH / "docs" / doc_name
    
    if not docs_path.exists():
        available_docs = list((NIR_TOOLS_PATH / "docs").glob("*.*"))
        return f"""
❌ 文档 '{doc_name}' 不存在

📁 可用文档：
{chr(10).join([f"  - {f.stem}" for f in available_docs])}

💡 使用方式：docs://文档名
"""
    
    try:
        with open(docs_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(docs_path, "r", encoding="gbk") as f:
            content = f.read()
    
    return f"""
# 📄 {doc_name} 文档

{content}

---
📍 文档路径：{docs_path}
📊 文档大小：{len(content)} 字符
"""


@mcp.resource("function://{category}/{func_name}")
def get_function_code(category: str, func_name: str) -> str:
    """
    获取函数源代码
    
    类别：
    - preprocessing: 预处理函数
    - analysis: 分析函数
    - visualization: 可视化函数
    
    使用：
    - function://preprocessing/savgol
    - function://analysis/pls
    - function://visualization/plot_spectrum
    """
    func_path = NIR_TOOLS_PATH / "functions" / category / f"{func_name}.m"
    
    if not func_path.exists():
        # 列出可用函数
        category_path = NIR_TOOLS_PATH / "functions" / category
        if category_path.exists():
            available = [f.stem for f in category_path.glob("*.m")]
            return f"""
❌ 函数 '{func_name}' 在 '{category}' 类别中不存在

📁 可用函数：
{chr(10).join([f"  - {func}" for func in available])}

💡 使用方式：function://{category}/函数名
"""
        else:
            return f"❌ 类别 '{category}' 不存在"
    
    with open(func_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # 提取 MATLAB 注释（帮助文档）
    lines = code.split("\n")
    help_text = []
    in_help = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # MATLAB 函数定义后的注释块
        if i == 0 and stripped.startswith("function"):
            continue
        
        if stripped.startswith("%"):
            help_text.append(stripped[1:].strip())
            in_help = True
        elif in_help and not stripped.startswith("%"):
            break
    
    # 提取函数签名
    func_signature = ""
    for line in lines:
        if line.strip().startswith("function"):
            func_signature = line.strip()
            break
    
    return f"""
# 🔧 {func_name}.m

## 函数签名
```matlab
{func_signature}
```

## 函数说明
{chr(10).join(help_text) if help_text else "❌ 该函数暂无说明注释"}

## 完整代码
```matlab
{code}
```

---
📍 文件路径：{func_path}
📊 代码行数：{len(lines)} 行
💡 提示：可以让 AI 解释代码逻辑、参数含义、使用场景
"""


@mcp.resource("example://{example_name}")
def get_example(example_name: str) -> str:
    """
    获取使用示例
    
    可用示例：
    - example_preprocess: 预处理完整流程
    - example_pls: PLS 回归示例
    - example_classification: 分类示例
    - example_visualization: 可视化示例
    
    使用：example://example_pls
    """
    example_path = NIR_TOOLS_PATH / "examples" / f"{example_name}.m"
    
    if not example_path.exists():
        available = [f.stem for f in (NIR_TOOLS_PATH / "examples").glob("*.m")]
        return f"""
❌ 示例 '{example_name}' 不存在

📁 可用示例：
{chr(10).join([f"  - {ex}" for ex in available])}

💡 使用方式：example://示例名
"""
    
    with open(example_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    return f"""
# 💡 {example_name} 使用示例

```matlab
{code}
```

---
📍 文件路径：{example_path}
💡 提示：
  - 可以让 AI 解释每一步的作用
  - 可以让 AI 根据你的数据修改示例
  - 可以让 AI 对比不同方法的示例
"""


@mcp.resource("list://functions")
def list_all_functions() -> str:
    """列出工具箱中的所有函数"""
    functions_dir = NIR_TOOLS_PATH / "functions"
    
    if not functions_dir.exists():
        return "❌ functions 目录不存在"
    
    result = "# 📚 近红外工具箱 - 所有函数\n\n"
    
    for category_dir in sorted(functions_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        
        result += f"## {category_dir.name}\n\n"
        
        m_files = list(category_dir.glob("*.m"))
        if not m_files:
            result += "（无函数）\n\n"
            continue
        
        for func_file in sorted(m_files):
            func_name = func_file.stem
            
            # 尝试读取第一行注释
            try:
                with open(func_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    first_comment = ""
                    for line in lines[1:6]:  # 在前 5 行找注释
                        if line.strip().startswith("%"):
                            first_comment = line.strip("% \n")
                            break
                
                result += f"- **{func_name}** - {first_comment}\n"
                result += f"  - 查看代码：`function://{category_dir.name}/{func_name}`\n"
            except:
                result += f"- **{func_name}**\n"
        
        result += "\n"
    
    result += "\n---\n"
    result += f"💡 使用方式：`function://类别/函数名`\n"
    result += f"📊 统计：共 {sum(1 for _ in functions_dir.rglob('*.m'))} 个函数\n"
    
    return result


@mcp.resource("list://examples")
def list_all_examples() -> str:
    """列出所有使用示例"""
    examples_dir = NIR_TOOLS_PATH / "examples"
    
    if not examples_dir.exists():
        return "❌ examples 目录不存在"
    
    result = "# 💡 使用示例列表\n\n"
    
    for example_file in sorted(examples_dir.glob("*.m")):
        example_name = example_file.stem
        
        # 尝试读取说明
        try:
            with open(example_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                description = ""
                for line in lines[:10]:
                    if line.strip().startswith("%"):
                        description = line.strip("% \n")
                        break
            
            result += f"- **{example_name}** - {description}\n"
            result += f"  - 查看示例：`example://{example_name}`\n\n"
        except:
            result += f"- **{example_name}**\n\n"
    
    result += "---\n"
    result += f"💡 使用方式：`example://示例名`\n"
    
    return result


# ==========================================
# 3. Tools: 搜索和查询功能
# ==========================================

@mcp.tool()
def search_function(keyword: str) -> str:
    """
    搜索包含关键词的函数
    
    Args:
        keyword: 搜索关键词（如 "smooth", "pls", "snv", "derivative"）
    
    Returns:
        匹配的函数列表及其简介
    
    示例：
        - search_function("smooth") → 查找所有平滑函数
        - search_function("normalize") → 查找标准化函数
    """
    functions_dir = NIR_TOOLS_PATH / "functions"
    results = []
    
    for m_file in functions_dir.rglob("*.m"):
        try:
            with open(m_file, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
        
        # 搜索关键词（不区分大小写）
        if keyword.lower() in content.lower():
            func_name = m_file.stem
            category = m_file.parent.name
            
            # 提取第一行注释作为简介
            lines = content.split("\n")
            description = ""
            for line in lines[1:6]:
                if line.strip().startswith("%"):
                    description = line.strip("% ")
                    break
            
            results.append({
                "name": func_name,
                "category": category,
                "description": description,
                "path": f"function://{category}/{func_name}"
            })
    
    if not results:
        return f"""
❌ 未找到包含 '{keyword}' 的函数

💡 提示：
  - 尝试更通用的关键词（如 "pre" 而非 "preprocessing"）
  - 检查拼写
  - 使用 list://functions 查看所有函数
"""
    
    output = f"# 🔍 搜索结果：'{keyword}'\n\n"
    output += f"找到 {len(results)} 个匹配的函数：\n\n"
    
    for r in results:
        output += f"## {r['name']} ({r['category']})\n"
        output += f"{r['description']}\n"
        output += f"📖 查看详情：`{r['path']}`\n\n"
    
    return output


@mcp.tool()
def explain_function(category: str, func_name: str, question: str = "") -> str:
    """
    详细解释一个函数的用法
    
    Args:
        category: 函数类别（preprocessing/analysis/visualization）
        func_name: 函数名称
        question: 具体问题（可选）
    
    Returns:
        函数的详细说明和代码，供 AI 进一步解释
    
    示例：
        - explain_function("preprocessing", "snv")
        - explain_function("analysis", "pls", "参数如何选择？")
    """
    func_path = NIR_TOOLS_PATH / "functions" / category / f"{func_name}.m"
    
    if not func_path.exists():
        return f"❌ 函数 {category}/{func_name} 不存在"
    
    with open(func_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    prompt = f"""
# 请详细解释以下 MATLAB 函数

## 函数信息
- 名称：{func_name}
- 类别：{category}
- 路径：{func_path}

## 源代码
```matlab
{code}
```

## 请解释
1. **函数作用** - 这个函数是做什么的？
2. **输入参数** - 每个参数的含义和类型
3. **输出结果** - 返回值的含义
4. **算法原理** - 底层实现的逻辑（如果有）
5. **使用场景** - 什么时候用这个函数？
6. **参数建议** - 常用的参数值
7. **注意事项** - 使用时需要注意什么
8. **相关函数** - 相似或配套的函数
"""
    
    if question:
        prompt += f"\n\n## 用户的具体问题\n{question}\n"
    
    return prompt


@mcp.tool()
def compare_methods(method1: str, method2: str, category: str = "preprocessing") -> str:
    """
    对比两种方法
    
    Args:
        method1: 第一种方法
        method2: 第二种方法
        category: 方法类别
    
    Returns:
        两种方法的对比分析提示
    
    示例：
        - compare_methods("snv", "msc", "preprocessing")
    """
    path1 = NIR_TOOLS_PATH / "functions" / category / f"{method1}.m"
    path2 = NIR_TOOLS_PATH / "functions" / category / f"{method2}.m"
    
    if not path1.exists():
        return f"❌ 方法 {method1} 不存在"
    if not path2.exists():
        return f"❌ 方法 {method2} 不存在"
    
    with open(path1, "r", encoding="utf-8") as f:
        code1 = f.read()
    with open(path2, "r", encoding="utf-8") as f:
        code2 = f.read()
    
    return f"""
# 请对比以下两种 {category} 方法

## 方法 1: {method1}

```matlab
{code1}
```

## 方法 2: {method2}

```matlab
{code2}
```

## 请对比分析
1. **原理对比** - 两种方法的算法原理有何不同？
2. **适用场景** - 分别适用于什么数据和任务？
3. **优缺点** - 各自的优势和劣势
4. **参数设置** - 参数选择有何差异？
5. **计算效率** - 速度和内存占用
6. **使用建议** - 在什么情况下选择哪个？

💡 如果用户提供了具体的数据特点，请给出更针对性的建议。
"""


# ==========================================
# 4. Prompts: 常见问题模板
# ==========================================

@mcp.prompt()
def how_to_preprocess(method: str = "savgol") -> str:
    """
    预处理方法使用指南
    
    Args:
        method: 预处理方法名称（savgol/snv/msc/sg/normalize）
    """
    return f"""
我想使用 **{method}** 方法对近红外光谱数据进行预处理。

请帮我：
1. 解释 {method} 方法的原理
2. 查看 `function://preprocessing/{method}` 的代码并解释
3. 说明参数的选择建议
4. 给出一个完整的使用示例（MATLAB 代码）
5. 说明该方法的适用场景和注意事项

【我的数据特点】
- 光谱范围：[请填写，如 1000-2500 nm]
- 样本数量：[请填写]
- 数据噪声：[低/中/高]
- 分析目标：[定性/定量]
"""


@mcp.prompt()
def build_model(method: str = "pls", task: str = "regression") -> str:
    """
    建模方法使用指南
    
    Args:
        method: 建模方法（pls/pcr/svm/lda/ann）
        task: 任务类型（regression/classification）
    """
    return f"""
我想使用 **{method}** 方法进行近红外光谱 {task} 建模。

请帮我：
1. 查看 `function://analysis/{method}` 的代码
2. 解释该方法的原理和适用场景
3. 说明关键参数的设置（如主成分数、核函数等）
4. 给出完整的建模流程代码（包括数据准备、建模、验证）
5. 推荐合适的模型评估指标
6. 说明常见问题和解决方法

【我的数据信息】
- 训练集大小：[样本数 × 波长数]
- 测试集大小：[样本数]
- 特征数量：[波长点数]
- 目标变量：[变量名称和范围]
- 预处理方法：[已使用的预处理]
"""


@mcp.prompt()
def troubleshoot_issue(problem_description: str = "") -> str:
    """
    问题诊断模板
    
    Args:
        problem_description: 问题描述
    """
    return f"""
我在使用近红外工具箱时遇到了问题：

【问题描述】
{problem_description if problem_description else "[请描述你的问题]"}

【请帮我】
1. 分析可能的原因
2. 查看相关函数的代码（如果需要）
3. 提供解决方案
4. 给出修正后的代码示例

【我的操作步骤】
1. [步骤 1]
2. [步骤 2]
3. ...

【错误信息】
[如果有错误提示，请粘贴在这里]
"""


@mcp.prompt()
def workflow_guide(task: str = "classification") -> str:
    """
    完整工作流程指南
    
    Args:
        task: 任务类型（classification/regression/exploratory）
    """
    return f"""
我想进行一个近红外光谱 {task} 分析，需要一个完整的工作流程。

请帮我设计一个完整流程，包括：

1. **数据预处理**
   - 推荐的预处理方法组合
   - 参数设置建议
   - 查看相关函数代码并解释

2. **特征选择**（可选）
   - 推荐的特征选择方法
   - 如何实现

3. **模型构建**
   - 推荐的建模方法
   - 参数优化策略
   - 查看建模函数代码

4. **模型评估**
   - 评估指标选择
   - 交叉验证方案

5. **结果可视化**
   - 推荐的图表类型
   - 查看可视化函数

6. **完整代码**
   - 提供一个可以直接运行的 MATLAB 脚本

【我的数据】
- 样本数：[训练集/测试集]
- 光谱范围：[波长范围]
- 目标变量：[变量描述]
"""


# ==========================================
# 5. 运行服务器
# ==========================================

if __name__ == "__main__":
    print("="*70, file=sys.stderr)
    print("🔬 NIR Tools MCP Server", file=sys.stderr)
    print("="*70, file=sys.stderr)
    print(f"📁 工具箱路径: {NIR_TOOLS_PATH}", file=sys.stderr)
    print(f"✅ 服务器已启动", file=sys.stderr)
    print("="*70, file=sys.stderr)
    
    # 使用 stdio 传输（适合 Claude Desktop）
    mcp.run(transport="stdio")
```

---

## 5. 配置部署

### 5.1 安装依赖

```bash
# 安装 MCP SDK
pip install "mcp[cli]"
```

---

### 5.2 修改配置

**在 `nir_tools_server.py` 中修改：**

```python
# ⚠️ 第 23 行：修改为你的工具箱路径
NIR_TOOLS_PATH = Path("~/Desktop/NIRTools").expanduser()
```

**确保你的路径结构包含：**
- `docs/` - 文档目录
- `functions/` - 函数代码目录
- `examples/` - 示例目录

---

### 5.3 测试 Server

```bash
# 运行 server（会等待输入）
python3 nir_tools_server.py
```

**测试方式 1：使用 MCP Inspector**

```bash
# 安装并运行 Inspector
npx -y @modelcontextprotocol/inspector

# 连接方式选择 "stdio"
# 命令填写：python3 /absolute/path/to/nir_tools_server.py
```

---

### 5.4 配置 Claude Desktop

**编辑配置文件：**

```bash
# macOS
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**添加配置：**

```json
{
  "mcpServers": {
    "nir-tools": {
      "command": "python3",
      "args": [
        "/Users/liam/Desktop/好用的工具/nir_tools_server.py"
      ]
    }
  }
}
```

**保存并重启 Claude Desktop**（必须完全退出，Cmd+Q）

---

## 6. 使用示例

### 6.1 查询函数列表

**你问：**
> "有哪些预处理函数？"

**Claude 会：**
1. 读取 `list://functions`
2. 列出所有预处理函数
3. 说明每个函数的作用

**示例回答：**
```
近红外工具箱提供以下预处理函数：

## preprocessing
- savgol - Savitzky-Golay 平滑
- snv - 标准正态变换
- msc - 多元散射校正
- sg - Savitzky-Golay 导数
- normalize - 归一化

你想了解哪个函数的详细用法？
```

---

### 6.2 查看函数详情

**你问：**
> "SNV 是怎么用的？"

**Claude 会：**
1. 调用 `explain_function("preprocessing", "snv")`
2. 读取 `function://preprocessing/snv`
3. 解释代码逻辑
4. 给出使用示例

**示例回答：**
```
SNV (Standard Normal Variate) 标准正态变换

【原理】
对每个样本的光谱进行标准化，消除光程差异...

【代码说明】
function [X_snv] = snv(X)
% 输入 X: n × p 矩阵（n 个样本，p 个波长）
% 输出 X_snv: 标准化后的矩阵

【使用示例】
% 加载数据
load('spectra.mat');

% SNV 预处理
X_preprocessed = snv(X);

% 继续后续分析...

【适用场景】
✅ 消除光程差异
✅ 处理散射效应
❌ 不适合有负值的光谱
```

---

### 6.3 对比不同方法

**你问：**
> "SNV 和 MSC 有什么区别？我该用哪个？"

**Claude 会：**
1. 调用 `compare_methods("snv", "msc", "preprocessing")`
2. 读取两个函数的代码
3. 对比分析
4. 给出建议

**示例回答：**
```
【SNV vs MSC 对比】

原理：
- SNV: 对每个样本单独标准化
- MSC: 基于参考光谱校正

适用场景：
- SNV: 样本间差异大
- MSC: 样本相对均匀

优缺点：
SNV:
  ✅ 简单快速
  ✅ 无需参考光谱
  ❌ 可能损失有用信息

MSC:
  ✅ 保留更多信息
  ✅ 物理意义更明确
  ❌ 需要选择参考光谱

【你的选择】
如果你的样本差异大 → SNV
如果你有代表性参考样本 → MSC
不确定 → 两个都试试，看模型效果
```

---

### 6.4 生成完整流程

**你问：**
> "给我一个 PLS 建模的完整流程"

**Claude 会：**
1. 读取 `example://example_pls`
2. 读取 `function://analysis/pls`
3. 结合最佳实践
4. 生成完整代码

**示例回答：**
```matlab
% ============================================
% 近红外光谱 PLS 建模完整流程
% ============================================

% 1. 加载数据
load('nir_data.mat');  % X: 光谱矩阵, Y: 目标变量

% 2. 数据划分
[n, p] = size(X);
train_idx = 1:floor(0.7*n);
test_idx = (floor(0.7*n)+1):n;

X_train = X(train_idx, :);
Y_train = Y(train_idx);
X_test = X(test_idx, :);
Y_test = Y(test_idx);

% 3. 预处理（推荐组合）
X_train = snv(X_train);      % SNV 标准化
X_train = savgol(X_train, 9, 2);  % SG 平滑 + 一阶导数

X_test = snv(X_test);
X_test = savgol(X_test, 9, 2);

% 4. PLS 建模
ncomp = 10;  % 主成分数
[model] = pls(X_train, Y_train, ncomp);

% 5. 预测
Y_pred = predict_pls(model, X_test);

% 6. 评估
R2 = corr(Y_test, Y_pred)^2;
RMSE = sqrt(mean((Y_test - Y_pred).^2));

fprintf('R² = %.4f\n', R2);
fprintf('RMSE = %.4f\n', RMSE);

% 7. 可视化
plot_scores(model);
plot_loadings(model);
```

---

### 6.5 使用 Prompt 模板

**在 Claude Desktop 中：**

1. 点击 "+" 图标
2. 选择 "Connectors"
3. 看到 "nir-tools" server
4. 选择 Prompt: "how_to_preprocess"
5. 填写参数：method = "snv"
6. Claude 自动生成完整的提问

---

## 7. 进阶功能

### 7.1 自动提取函数依赖

```python
@mcp.tool()
def get_dependencies(category: str, func_name: str) -> str:
    """查找函数调用的其他函数"""
    func_path = NIR_TOOLS_PATH / "functions" / category / f"{func_name}.m"
    
    with open(func_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # 查找函数调用（简单正则）
    import re
    calls = re.findall(r'\b([a-z_]+)\s*\(', code)
    
    # 过滤掉 MATLAB 内置函数
    matlab_builtins = {'mean', 'std', 'size', 'zeros', 'ones', 'plot', 'figure'}
    custom_calls = [c for c in calls if c not in matlab_builtins]
    
    return f"""
# {func_name} 的依赖函数

## 调用的自定义函数
{chr(10).join([f"- {c}" for c in set(custom_calls)])}

💡 提示：你可能需要先了解这些函数
"""
```

---

### 7.2 生成 Python 等效代码

```python
@mcp.prompt()
def matlab_to_python(category: str, func_name: str) -> str:
    """将 MATLAB 函数转换为 Python"""
    return f"""
请将以下 MATLAB 函数转换为等效的 Python 代码：

【MATLAB 代码】
查看：`function://{category}/{func_name}`

【转换要求】
1. 使用 NumPy/SciPy 实现
2. 保持相同的输入输出接口
3. 添加类型提示和文档字符串
4. 确保算法逻辑一致

【输出格式】
```python
import numpy as np
from typing import ...

def {func_name}(...) -> ...:
    \"\"\"
    函数说明
    
    Args:
        ...
    
    Returns:
        ...
    \"\"\"
    # 实现代码
    ...
```
"""
```

---

### 7.3 版本历史（如果使用 Git）

```python
@mcp.tool()
def get_function_history(category: str, func_name: str) -> str:
    """获取函数的修改历史"""
    import subprocess
    
    func_path = f"functions/{category}/{func_name}.m"
    
    result = subprocess.run(
        ["git", "log", "--oneline", "--", func_path],
        cwd=NIR_TOOLS_PATH,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return "❌ 无法获取历史（可能未使用 Git）"
    
    return f"""
# {func_name} 修改历史

```
{result.stdout}
```

💡 可以使用 `git show <commit_id>` 查看具体改动
"""
```

---

### 7.4 性能基准测试

```python
@mcp.resource("benchmark://{func_name}")
def get_benchmark(func_name: str) -> str:
    """获取函数的性能测试结果"""
    benchmark_dir = NIR_TOOLS_PATH / "benchmarks"
    benchmark_file = benchmark_dir / f"{func_name}_benchmark.txt"
    
    if not benchmark_file.exists():
        return f"""
❌ 暂无 {func_name} 的性能测试数据

💡 你可以创建基准测试：
```matlab
% 测试 {func_name} 性能
n_samples = [100, 500, 1000, 5000];
n_vars = [100, 500, 1000];

for n = n_samples
    for p = n_vars
        X = randn(n, p);
        tic;
        result = {func_name}(X);
        t = toc;
        fprintf('n=%d, p=%d: %.4f 秒\\n', n, p, t);
    end
end
```
"""
    
    with open(benchmark_file, "r") as f:
        content = f.read()
    
    return f"# {func_name} 性能基准\n\n{content}"
```

---

## 8. 故障排查

### 8.1 Server 无法启动

#### 问题 1：找不到模块

```
ModuleNotFoundError: No module named 'mcp'
```

**解决：**
```bash
pip install "mcp[cli]"
```

---

#### 问题 2：路径不存在

```
❌ 错误：工具箱路径不存在: /Users/liam/Desktop/NIRTools
```

**解决：**
1. 检查路径是否正确
2. 修改 `nir_tools_server.py` 第 23 行
3. 使用绝对路径

---

### 8.2 Claude Desktop 无法连接

#### 问题 1：Server 未显示在 Connectors

**排查步骤：**

```bash
# 1. 检查配置文件
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. 检查日志
tail -f ~/Library/Logs/Claude/mcp*.log

# 3. 测试 server 是否能运行
python3 nir_tools_server.py
# （会等待输入，Ctrl+C 退出）
```

**常见原因：**
- ❌ 路径不是绝对路径
- ❌ Python 路径错误
- ❌ 配置文件格式错误
- ❌ 未重启 Claude Desktop

---

#### 问题 2：Server 显示但无法使用

**检查：**
1. Server 日志是否有错误
2. 工具箱路径是否正确
3. 文件权限是否正确

```bash
# 检查文件权限
ls -la ~/Desktop/NIRTools/functions/
```

---

### 8.3 编码问题

#### 问题：中文乱码

**原因：** MATLAB .m 文件可能是 GBK 编码

**解决：**
```python
# 在 get_function_code 函数中
try:
    with open(func_path, "r", encoding="utf-8") as f:
        code = f.read()
except UnicodeDecodeError:
    # 尝试 GBK 编码
    with open(func_path, "r", encoding="gbk") as f:
        code = f.read()
```

---

## 9. 实际应用场景

### 场景 1：快速查函数

**你：** "有没有平滑函数？"

**Claude：**
```
我帮你搜索了包含 "smooth" 的函数：

1. savgol (preprocessing)
   - Savitzky-Golay 平滑和导数
   - function://preprocessing/savgol

2. moving_average (preprocessing)
   - 移动平均平滑
   - function://preprocessing/moving_average

你想了解哪个的详细用法？
```

---

### 场景 2：对比方法

**你：** "PLS 和 PCR 的区别？"

**Claude：**
```
【PLS vs PCR 对比】

原理差异：
- PLS: 同时考虑 X 和 Y 的方差，目标是最大化协方差
- PCR: 只考虑 X 的方差，然后回归

优缺点：
PLS:
  ✅ 预测能力通常更好
  ✅ 需要更少的主成分
  ❌ 解释性稍弱

PCR:
  ✅ 解释性更强
  ✅ 计算简单
  ❌ 可能需要更多主成分

【选择建议】
- 预测任务 → PLS（推荐）
- 探索性分析 → PCR
- 大多数情况 → PLS
```

---

### 场景 3：完整工作流

**你：** "给我一个分类任务的完整流程"

**Claude：**
1. 使用 Prompt: `workflow_guide("classification")`
2. 读取相关函数
3. 读取示例代码
4. 生成定制化流程

**输出：**
完整的 MATLAB 代码 + 详细注释

---

### 场景 4：问题诊断

**你：** "我的 PLS 模型 R² 只有 0.3，怎么办？"

**Claude：**
```
【诊断 PLS 模型效果差】

可能原因：
1. 预处理不足
   - 尝试：SNV + SG 导数
   
2. 主成分数不合适
   - 查看：交叉验证曲线
   - 建议：使用 CV 自动选择

3. 异常值影响
   - 检查：PCA 得分图
   - 处理：移除异常样本

4. 特征冗余
   - 尝试：变量筛选

【改进代码】
% 1. 增强预处理
X = snv(X);
X = savgol(X, 9, 2, 1);  % 一阶导数

% 2. 交叉验证选择主成分
ncomp_opt = pls_cv(X_train, Y_train, 1:20);

% 3. 重新建模
model = pls(X_train, Y_train, ncomp_opt);
```

---

## 10. 扩展建议

### 10.1 添加更多类别

```python
# 如果你的工具箱还有其他类别
@mcp.resource("function://{category}/{func_name}")
def get_function_code(category: str, func_name: str) -> str:
    """
    支持的类别：
    - preprocessing
    - analysis
    - visualization
    - calibration        # ✅ 新增：校准方法
    - feature_selection  # ✅ 新增：特征选择
    - outlier_detection  # ✅ 新增：异常检测
    """
    # ... 相同的代码 ...
```

---

### 10.2 支持多种文件格式

```python
@mcp.resource("data://{dataset_name}")
def get_dataset_info(dataset_name: str) -> str:
    """读取数据集信息"""
    data_path = NIR_TOOLS_PATH / "data" / dataset_name
    
    # 支持 .mat, .csv, .txt
    if data_path.with_suffix('.mat').exists():
        # 读取 .mat 文件信息
        from scipy.io import loadmat
        data = loadmat(data_path.with_suffix('.mat'))
        return f"数据集信息：\n{data.keys()}"
    
    # ... 其他格式
```

---

### 10.3 集成到你的 Seminar 系统

**可能性：** 在 Seminar 分析论文时，如果论文用到近红外方法，AI 可以自动查阅你的工具箱！

```python
# 在 seminar/main.py 中添加 NIR Tools
from langchain_mcp_adapters import MCPServer

nir_mcp = MCPServer(
    command="python3",
    args=["/path/to/nir_tools_server.py"]
)

# 将 MCP 工具添加到 Agent
tools = nir_mcp.get_tools()
llm_with_tools = llm.bind_tools(tools)
```

---

## 11. 完整文件清单

### 需要创建的文件

```
/Users/liam/Desktop/好用的工具/
├── nir_tools_server.py          # MCP Server 主程序
├── test_nir_mcp.py              # 测试脚本
└── README_NIR_MCP.md            # 说明文档
```

---

### 需要配置的文件

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## 12. 快速开始

### Step 1: 创建 Server

```bash
# 1. 创建文件
cd /Users/liam/Desktop/好用的工具
touch nir_tools_server.py

# 2. 复制上面的完整代码到 nir_tools_server.py

# 3. 修改工具箱路径（第 23 行）
# NIR_TOOLS_PATH = Path("~/Desktop/NIRTools").expanduser()
```

---

### Step 2: 安装依赖

```bash
pip install "mcp[cli]"
```

---

### Step 3: 测试 Server

```bash
# 测试运行（Ctrl+C 退出）
python3 nir_tools_server.py

# 看到以下输出表示成功：
# ======================================================================
# 🔬 NIR Tools MCP Server
# ======================================================================
# 📁 工具箱路径: /Users/liam/Desktop/NIRTools
# ✅ 服务器已启动
# ======================================================================
```

---

### Step 4: 配置 Claude Desktop

```bash
# 1. 编辑配置
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. 添加以下内容（修改路径）
{
  "mcpServers": {
    "nir-tools": {
      "command": "python3",
      "args": [
        "/Users/liam/Desktop/好用的工具/nir_tools_server.py"
      ]
    }
  }
}

# 3. 保存文件

# 4. 完全退出 Claude Desktop（Cmd+Q）

# 5. 重新打开 Claude Desktop
```

---

### Step 5: 验证连接

1. 打开 Claude Desktop
2. 点击 "+" 图标
3. 查看 "Connectors" 菜单
4. 应该看到 "nir-tools" server

**如果看到了：** ✅ 配置成功！

**如果没看到：** 查看 [故障排查](#8-故障排查)

---

### Step 6: 开始使用

**在 Claude 中提问：**

```
# 测试 1：列出函数
"近红外工具箱有哪些函数？"

# 测试 2：查看函数
"SNV 标准化是怎么实现的？"

# 测试 3：对比方法
"SNV 和 MSC 有什么区别？"

# 测试 4：完整流程
"给我一个 PLS 建模的完整代码"
```

---

## 13. 示例：完整 Server 代码

**文件位置：** `/Users/liam/Desktop/好用的工具/nir_tools_server.py`

（完整代码见 [4. 完整实现](#4-完整实现) 部分）

**关键点：**
1. ✅ **Resources** - 暴露文档、代码、示例
2. ✅ **Tools** - 搜索、解释、对比
3. ✅ **Prompts** - 常见问题模板
4. ✅ **错误处理** - 文件不存在时给出提示
5. ✅ **编码兼容** - 支持 UTF-8 和 GBK

---

## 14. 测试脚本

**文件：`test_nir_mcp.py`**

```python
#!/usr/bin/env python3
"""测试 NIR Tools MCP Server"""

import subprocess
import json
import sys

def test_server():
    print("🧪 测试 NIR Tools MCP Server\n")
    
    # 测试 1：Server 能否启动
    print("1️⃣ 测试 Server 启动...")
    try:
        proc = subprocess.Popen(
            ["python3", "nir_tools_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送 initialize 请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        # 等待响应（最多 5 秒）
        import select
        ready, _, _ = select.select([proc.stdout], [], [], 5)
        
        if ready:
            response = proc.stdout.readline()
            print("   ✅ Server 启动成功")
            print(f"   响应：{response[:100]}...")
        else:
            print("   ❌ Server 无响应")
        
        proc.terminate()
        
    except Exception as e:
        print(f"   ❌ 启动失败：{e}")
        return False
    
    # 测试 2：配置文件检查
    print("\n2️⃣ 检查 Claude Desktop 配置...")
    config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    
    if not config_path.exists():
        print("   ⚠️  配置文件不存在")
        print(f"   请创建：{config_path}")
    else:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        if "nir-tools" in config.get("mcpServers", {}):
            print("   ✅ 已配置 nir-tools server")
        else:
            print("   ⚠️  未配置 nir-tools server")
            print("   请添加 server 配置")
    
    print("\n✅ 测试完成！")
    return True

if __name__ == "__main__":
    test_server()
```

---

## 15. 最佳实践

### 15.1 文档组织

**建议的文档结构：**

```markdown
# preprocessing.md

## SNV (Standard Normal Variate)

### 原理
对每个样本的光谱进行标准化...

### 参数
- 无参数

### 使用场景
- 消除光程差异
- 处理散射效应

### 注意事项
- 不适合有负值的光谱
- 会损失部分信息

### 相关方法
- MSC: 多元散射校正
- normalize: 简单归一化

---

## MSC (Multiplicative Scatter Correction)

...
```

---

### 15.2 代码注释规范

**MATLAB 函数注释示例：**

```matlab
function [X_snv] = snv(X)
% SNV - Standard Normal Variate 标准正态变换
%
% 功能：
%   对每个样本的光谱进行标准化，消除光程和散射的影响
%
% 输入：
%   X - n×p 矩阵（n 个样本，p 个波长点）
%
% 输出：
%   X_snv - 标准化后的光谱矩阵
%
% 示例：
%   load('spectra.mat');
%   X_preprocessed = snv(X);
%
% 参考文献：
%   Barnes et al. (1989) Standard Normal Variate Transformation
%
% 作者：Liam
% 日期：2026-01-27

% 计算每个样本的均值和标准差
means = mean(X, 2);
stds = std(X, 0, 2);

% 标准化
X_snv = (X - means) ./ stds;

end
```

---

### 15.3 示例代码规范

**完整示例结构：**

```matlab
% ============================================
% 示例：PLS 回归完整流程
% 功能：演示从数据加载到模型评估的完整过程
% 作者：Liam
% 日期：2026-01-27
% ============================================

%% 1. 清理环境
clear; clc; close all;

%% 2. 加载数据
load('corn_nir.mat');  % X: 光谱, Y: 蛋白质含量

%% 3. 数据划分
% ... 代码 + 注释 ...

%% 4. 预处理
% ... 代码 + 注释 ...

%% 5. 模型构建
% ... 代码 + 注释 ...

%% 6. 模型评估
% ... 代码 + 注释 ...

%% 7. 可视化
% ... 代码 + 注释 ...
```

---

## 16. 维护和更新

### 16.1 添加新函数

当你添加新函数时：

1. **放到对应目录**
   ```
   NIRTools/functions/preprocessing/new_method.m
   ```

2. **添加注释**（参考 15.2 规范）

3. **重启 Claude Desktop**
   - MCP Server 会自动识别新文件
   - 无需修改 server 代码

---

### 16.2 更新文档

当你更新文档时：

1. **直接修改 .md 文件**
   ```
   NIRTools/docs/preprocessing.md
   ```

2. **重启 Claude Desktop**
   - AI 会自动读取最新内容

---

### 16.3 版本管理

**建议使用 Git：**

```bash
cd ~/Desktop/NIRTools
git init
git add .
git commit -m "Initial commit: NIR Tools v1.0"

# 每次修改后
git add functions/preprocessing/new_method.m
git commit -m "Add new_method for X preprocessing"
```

**好处：**
- ✅ 可以使用 `get_function_history` 工具
- ✅ 追踪每个函数的改动历史
- ✅ 方便回退

---

## 17. 总结

### 17.1 为什么 MCP 适合你

| 你的需求 | MCP 的解决方案 |
|---------|---------------|
| 查文档费力 | AI 自动读取 docs:// |
| 看代码不直观 | AI 解释 function:// |
| 记不住用法 | 直接提问，AI 查阅 |
| 多文件切换 | AI 帮你整合信息 |
| 对比方法难 | AI 对比分析 |

---

### 17.2 实现成本

**时间成本：**
- 创建 Server：30 分钟
- 整理工具箱结构：1-2 小时
- 配置 Claude：5 分钟

**技术门槛：**
- ✅ 会基本的 Python（复制粘贴即可）
- ✅ 了解你的工具箱结构
- ✅ 无其他要求

---

### 17.3 预期收益

**使用场景频率：**
- 查询函数用法：每天 5-10 次 → 节省 20-30 分钟/天
- 对比不同方法：每周 2-3 次 → 节省 1-2 小时/周
- 生成完整流程：每月 1-2 次 → 节省 2-3 小时/月

**总节省时间：** 约 **10-15 小时/月**

---

## 18. 下一步行动

### 立即开始（推荐）

```bash
# 1. 创建 server 文件
cd /Users/liam/Desktop/好用的工具
nano nir_tools_server.py
# 粘贴完整代码

# 2. 修改工具箱路径（第 23 行）

# 3. 安装依赖
pip install "mcp[cli]"

# 4. 测试运行
python3 nir_tools_server.py
# （Ctrl+C 退出）

# 5. 配置 Claude
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 6. 重启 Claude Desktop

# 7. 开始提问！
```

---

### 或者先试试 Demo

如果你不确定效果，我可以帮你：
1. 创建一个简化版 Demo
2. 用模拟数据测试
3. 验证可行性
4. 再实现完整版

---

## 19. 常见问题 FAQ

### Q1: 我的工具箱结构和你假设的不一样怎么办？

**A:** 修改 `nir_tools_server.py` 中的路径即可：

```python
# 假设你的结构是：
# NIRTools/
#   ├── m_files/        # 而不是 functions/
#   └── doc/            # 而不是 docs/

# 修改代码：
func_path = NIR_TOOLS_PATH / "m_files" / category / f"{func_name}.m"
docs_path = NIR_TOOLS_PATH / "doc" / f"{doc_name}.md"
```

---

### Q2: 我的 .m 文件没有详细注释怎么办？

**A:** 没关系！AI 可以直接阅读代码：

```
你："SNV 函数是怎么工作的？"

Claude:
1. 读取 function://preprocessing/snv
2. 分析代码逻辑
3. 解释给你听（即使没有注释）
```

**建议：** 逐步添加注释，每次用 AI 解释后，把解释加到注释里

---

### Q3: 可以在 Cursor 中使用吗？

**A:** 可以！Cursor 也支持 MCP（如果配置了）

**但更推荐：** 在 Claude Desktop 中使用，因为：
- ✅ Claude Desktop 是专门的 MCP 客户端
- ✅ UI 更友好
- ✅ 配置更简单

---

### Q4: 会不会很慢？

**A:** 不会！

**速度：**
- 读取文档：< 1 秒
- 读取代码：< 1 秒
- 搜索函数：< 2 秒

**原因：** 所有文件都在本地，不需要网络请求

---

### Q5: 可以添加搜索功能吗？

**A:** 已经包含！

```python
@mcp.tool()
def search_function(keyword: str) -> str:
    """搜索包含关键词的函数"""
    # 在所有 .m 文件中搜索
```

**使用：**
```
你："有没有平滑函数？"
Claude 自动调用：search_function("smooth")
```

---

## 20. 附录

### A. MCP 官方资源

- 官方网站：https://modelcontextprotocol.io/
- Python SDK：https://modelcontextprotocol.github.io/python-sdk/
- 快速开始：https://modelcontextprotocol.io/quickstart/server
- GitHub：https://github.com/modelcontextprotocol

---

### B. 相关工具

- **MCP Inspector** - 调试 MCP Server
  ```bash
  npx -y @modelcontextprotocol/inspector
  ```

- **Claude Desktop** - MCP 客户端
  - 下载：https://claude.ai/download

---

### C. 常用命令

```bash
# 安装 MCP
pip install "mcp[cli]"

# 运行 Server
python3 nir_tools_server.py

# 测试 Server
npx -y @modelcontextprotocol/inspector

# 查看 Claude 日志
tail -f ~/Library/Logs/Claude/mcp*.log

# 编辑 Claude 配置
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

---

## 🎉 结语

通过创建 NIR Tools MCP Server，你可以：

- ✅ 让 AI 成为你的工具箱助手
- ✅ 快速查询任何函数的用法
- ✅ 对比不同方法的优缺点
- ✅ 生成完整的分析流程
- ✅ 节省大量查文档的时间

**投入：** 1-2 小时设置  
**收益：** 每月节省 10-15 小时

**立即开始，让 AI 帮你管理工具箱！** 🚀

---

*文档创建时间：2026-01-27*  
*作者：Liam*  
*适用于：MATLAB 近红外分析工具箱*