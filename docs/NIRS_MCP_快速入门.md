# 🚀 NIRS-Toolbox MCP Server 快速开始指南

**创建日期**: 2026-01-27  
**状态**: ✅ 代码已完成，待部署

---

## 📋 已完成的文件

✅ `/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py` - MCP服务器主程序  
✅ `/Users/liam/Desktop/好用的工具/NIRS-Toolbox_MCP实现方案.md` - 完整技术文档  
✅ `/Users/liam/Desktop/好用的工具/test_nirs_mcp.py` - 测试脚本  

---

## 🎯 3步部署

### Step 1: 安装MCP依赖

由于你的系统使用外部管理的Python环境，选择以下方式之一：

#### 方式A: 使用pipx（推荐）

```bash
# 1. 安装pipx（如果没有）
brew install pipx

# 2. 安装mcp
pipx install mcp
```

#### 方式B: 使用虚拟环境

```bash
# 1. 创建虚拟环境
cd /Users/liam/Desktop/好用的工具
python3 -m venv nirs_mcp_env

# 2. 激活虚拟环境
source nirs_mcp_env/bin/activate

# 3. 安装mcp
pip install "mcp[cli]"
```

#### 方式C: 使用--break-system-packages（不推荐）

```bash
pip3 install --break-system-packages "mcp[cli]"
```

---

### Step 2: 测试服务器

```bash
cd /Users/liam/Desktop/好用的工具

# 如果使用虚拟环境，先激活
# source nirs_mcp_env/bin/activate

# 运行测试
python3 test_nirs_mcp.py
```

**预期输出**:
```
🧪 测试 NIRS-Toolbox MCP Server

1️⃣ 检查服务器文件...
   ✅ 文件存在
2️⃣ 检查工具箱路径...
   ✅ 工具箱路径存在
   ✅ +nirs 命名空间: 725 个.m文件
   ✅ demos 目录: 14 个示例
3️⃣ 检查依赖...
   ✅ mcp 模块已安装
4️⃣ 测试服务器启动...
   ✅ 服务器启动成功
5️⃣ 检查 Claude Desktop 配置...
   ⚠️  未配置 nirs-toolbox server
```

---

### Step 3: 配置Claude Desktop

#### 3.1 创建/编辑配置文件

```bash
# 创建目录（如果不存在）
mkdir -p ~/Library/Application\ Support/Claude

# 编辑配置文件
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### 3.2 添加配置

**如果使用普通Python安装**:
```json
{
  "mcpServers": {
    "nirs-toolbox": {
      "command": "python3",
      "args": [
        "/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py"
      ]
    }
  }
}
```

**如果使用虚拟环境**:
```json
{
  "mcpServers": {
    "nirs-toolbox": {
      "command": "/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3",
      "args": [
        "/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py"
      ]
    }
  }
}
```

#### 3.3 重启Claude Desktop

```bash
# 完全退出Claude（Cmd+Q）
# 然后重新打开Claude Desktop
```

---

## ✅ 验证安装

### 在Claude Desktop中测试

打开Claude Desktop，尝试以下问题：

#### 测试1: 查看模块分类
```
NIRS工具箱有哪些模块分类？
```

**预期**: Claude会列出所有模块类别（modules, io, core等）

#### 测试2: 查看具体模块
```
BeerLambertLaw模块是做什么的？
```

**预期**: Claude会读取模块代码并解释Beer-Lambert定律的实现

#### 测试3: 搜索功能
```
有没有带通滤波的函数？
```

**预期**: Claude会搜索并找到BandPassFilter等相关模块

#### 测试4: 查看示例
```
有GLM分析的完整示例吗？
```

**预期**: Claude会列出相关demo并提供代码

---

## 🔧 故障排查

### 问题1: MCP模块安装失败

**症状**:
```
❌ mcp 模块未安装
```

**解决**:
- 使用pipx: `brew install pipx && pipx install mcp`
- 或使用虚拟环境（见Step 1方式B）

---

### 问题2: Claude中看不到nirs-toolbox server

**排查步骤**:

1. **检查配置文件是否正确**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. **检查JSON格式**
- 确保没有语法错误
- 使用在线JSON验证器检查

3. **检查路径是否正确**
```bash
# 测试服务器能否直接运行
python3 /Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py
# 应该看到 "✅ 服务器已启动"
# Ctrl+C 退出
```

4. **查看Claude日志**
```bash
# 查看最新日志
tail -100 ~/Library/Logs/Claude/mcp*.log
```

5. **确保完全重启了Claude**
- 使用 Cmd+Q 完全退出
- 不要只是关闭窗口

---

### 问题3: 工具箱路径错误

**症状**:
```
❌ 错误：工具箱路径不存在
```

**解决**:
编辑 `nirs_toolbox_mcp.py` 第23行，确认路径正确：
```python
NIRS_TOOLBOX_PATH = Path("/Users/liam/Desktop/好用的工具/nirs-toolbox").expanduser()
```

---

### 问题4: Python版本问题

**检查Python版本**:
```bash
python3 --version
# 应该是 3.8 或更高版本
```

如果版本太低，使用Homebrew更新：
```bash
brew install python@3.11
```

---

## 💡 使用技巧

### 1. 快速查找模块

**场景**: 我想找滤波相关的函数

**提问**:
```
搜索一下包含filter的模块
```

**Claude会**: 自动调用 `search_module("filter")` 并展示结果

---

### 2. 学习工作流

**场景**: 我想做GLM分析但不知道流程

**提问**:
```
给我一个GLM分析的完整工作流
```

**Claude会**: 
1. 调用 `find_workflow("glm")`
2. 列出需要的模块
3. 生成完整MATLAB代码

---

### 3. 对比方法

**场景**: 不知道该用哪个方法

**提问**:
```
OpticalDensity和BeerLambertLaw有什么区别？
```

**Claude会**:
1. 调用 `compare_modules(...)`
2. 读取两个模块代码
3. 详细对比分析

---

### 4. 查看示例代码

**场景**: 想看官方例子

**提问**:
```
有连接性分析的示例吗？
```

**Claude会**:
1. 搜索demo列表
2. 找到 `fnirs_connectivity_demo`
3. 展示完整代码并解释

---

## 📊 功能列表

### Resources（可查询的资源）

| 资源URI | 说明 | 示例 |
|---------|-----|------|
| `list://categories` | 列出所有模块分类 | Claude会自动调用 |
| `category://modules` | 查看某个类别的所有模块 | 查看modules类别 |
| `module://modules/AR_IRLS` | 查看具体模块详情 | 查看AR_IRLS模块 |
| `list://demos` | 列出所有示例 | 列出demo列表 |
| `demo://fnirs_analysis_demo` | 查看具体示例代码 | 查看分析示例 |

### Tools（可调用的工具）

| 工具名 | 功能 | 参数 |
|-------|-----|------|
| `search_module` | 搜索模块 | keyword（关键词） |
| `find_workflow` | 查找工作流 | task（任务类型） |
| `compare_modules` | 对比两个模块 | name1, name2 |

### Prompts（预设模板）

| 模板名 | 用途 |
|-------|-----|
| `how_to_preprocess` | 预处理指南 |
| `how_to_glm_analysis` | GLM分析指南 |
| `how_to_load_data` | 数据加载指南 |
| `build_pipeline` | 构建分析流水线 |

---

## 📈 预期收益

| 任务 | 传统方式 | 使用MCP | 节省 |
|-----|---------|---------|-----|
| 查找函数 | 5-10分钟 | 10秒 | 95% |
| 理解模块 | 10-20分钟 | 1分钟 | 90% |
| 构建流程 | 30-60分钟 | 2-3分钟 | 95% |
| 学习示例 | 15-30分钟 | 1-2分钟 | 93% |

**每天节省**: 1-2小时  
**每周节省**: 5-10小时  
**每月节省**: 20-40小时

---

## 📚 相关文档

- **技术文档**: `/Users/liam/Desktop/好用的工具/NIRS-Toolbox_MCP实现方案.md`
- **原始指南**: `/Users/liam/Desktop/好用的工具/MCP近红外工具箱实现指南_2026-01-27.md`
- **服务器代码**: `/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py`

---

## 🎯 下一步

### 立即行动（5分钟）

```bash
# 1. 安装依赖（选择一种方式）
brew install pipx && pipx install mcp

# 2. 测试服务器
cd /Users/liam/Desktop/好用的工具
python3 test_nirs_mcp.py

# 3. 配置Claude
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
# 粘贴配置（见Step 3.2）

# 4. 重启Claude Desktop
# Cmd+Q 完全退出，然后重新打开

# 5. 测试
# 在Claude中问："NIRS工具箱有哪些模块？"
```

### 如果遇到问题

1. 查看本文档的"故障排查"部分
2. 运行测试脚本获取详细信息
3. 检查Claude日志文件

---

## 🎉 完成标志

当你在Claude Desktop中看到以下内容时，说明配置成功：

**你问**: "NIRS工具箱有哪些模块？"

**Claude答**: 
```
# 🧠 NIRS-Toolbox 模块分类

工具箱共包含 19 个主要类别：

## modules (83 个文件)
- 查看详情：category://modules

## util (108 个文件)
- 查看详情：category://util

...
```

**恭喜！🎊 你的NIRS-Toolbox MCP Server已经成功运行！**

---

*快速开始指南 v1.0*  
*创建时间：2026-01-27*  
*作者：Liam*
