# 👤 Huppert MCP - 用户使用指南

**面向**: 其他用户  
**难度**: ⭐⭐ 中等  
**时间**: 15分钟

---

## 📋 目录

1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [配置 Cursor](#配置-cursor)
4. [功能介绍](#功能介绍)
5. [使用示例](#使用示例)
6. [常见问题](#常见问题)
7. [进阶使用](#进阶使用)

---

## 系统要求

### 必需
- ✅ **Python 3.10+**
- ✅ **Cursor IDE**（最新版）
- ✅ **NIRS-Toolbox**（完整代码库）
- ✅ **macOS/Linux**（Windows需WSL）

### 可选
- Git（用于版本管理）
- Docker（用于容器化部署）

---

## 安装步骤

### 方法1: 自动安装（推荐）⭐

```bash
# 1. 解压或克隆项目
cd huppert_mcp

# 2. 运行安装脚本
./setup.sh

# 脚本会提示你输入 NIRS-Toolbox 路径
# 例如: /Users/yourname/projects/nirs-toolbox
```

**自动安装会做这些事：**
- ✅ 检查 Python 环境
- ✅ 创建虚拟环境（`venv/`）
- ✅ 安装所有依赖
- ✅ 生成配置文件
- ✅ 测试运行
- ✅ 生成 Cursor 配置示例

---

### 方法2: 手动安装

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 设置环境变量
export NIRS_TOOLBOX_PATH="/path/to/your/nirs-toolbox"

# 5. 测试运行
python3 nirs_toolbox_mcp.py
```

---

## 配置 Cursor

### Step 1: 打开配置文件

```bash
# macOS/Linux
open ~/.cursor/mcp.json

# 如果文件不存在，创建它
mkdir -p ~/.cursor
touch ~/.cursor/mcp.json
```

---

### Step 2: 添加 MCP 配置

将以下内容添加到 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "huppert": {
      "name": "Huppert Lab NIRS Toolbox",
      "command": "/完整路径/huppert_mcp/venv/bin/python3",
      "args": [
        "/完整路径/huppert_mcp/nirs_toolbox_mcp.py"
      ],
      "env": {
        "NIRS_TOOLBOX_PATH": "/完整路径/nirs-toolbox"
      }
    }
  }
}
```

**⚠️ 重要：替换路径**
- 将 `/完整路径/huppert_mcp/` 替换为你的实际路径
- 将 `/完整路径/nirs-toolbox` 替换为 NIRS-Toolbox 路径

**💡 提示：**
- 自动安装会生成 `cursor_mcp_config.json`，直接复制内容即可！

---

### Step 3: 重启 Cursor

```
1. Cmd+Q 完全退出 Cursor
2. 等待10秒（确保进程完全退出）
3. 重新打开 Cursor
```

---

### Step 4: 验证安装

在 Cursor Chat 中输入：

```
@huppert
```

如果看到 "Huppert Lab NIRS Toolbox"，说明安装成功！✅

---

## 功能介绍

### 🔍 Resources（资源）

| 资源 | 用途 | 示例 |
|------|------|------|
| `category://` | 列出所有模块类别 | 查看有哪些功能模块 |
| `module://` | 查看特定模块 | 查看 BandPassFilter |
| `demo://` | 获取示例代码 | 查看演示脚本 |

---

### 🛠️ Tools（工具）

| 工具 | 功能 | 推荐场景 |
|------|------|---------|
| **search_module** | 搜索模块 | 不知道模块名时 |
| **get_module_details** ⭐ | 获取完整模块信息 | 需要详细文档时 |
| **find_workflow** | 查找工作流 | 需要流程建议时 |
| **compare_modules** | 对比模块 | 选择方案时 |

---

### 💬 Prompts（提示）

| 提示 | 主题 | 适用场景 |
|------|------|---------|
| `how_to_preprocess` | 预处理指南 | 数据预处理 |
| `how_to_glm_analysis` | GLM分析 | 统计分析 |
| `how_to_load_data` | 数据加载 | 读取数据 |
| `build_pipeline` | 构建流水线 | 完整流程 |

---

## 使用示例

### 示例1: 基础查询

```
问: @huppert BandPassFilter
答: 返回 BandPassFilter 的基本信息
```

---

### 示例2: 详细查询（推荐）⭐

```
问: @huppert 详细介绍 AR_IRLS
答: 返回完整文档，包括：
   - 类描述
   - 属性表格（类型、默认值、说明）
   - 方法列表（签名、参数、注释）
   - 使用示例
   - 相关模块推荐
```

---

### 示例3: 搜索功能

```
问: @huppert 有哪些滤波模块？
答: 列出所有滤波相关模块：
   - BandPassFilter
   - WaveletFilter
   - FilterDesign
   ...
```

---

### 示例4: 工作流推荐

```
问: @huppert 预处理的标准流程是什么？
答: 返回完整预处理流程：
   1. 加载数据
   2. 质量检查
   3. 去运动伪迹
   4. 滤波
   5. 转换为血氧浓度
   + 完整代码示例
```

---

### 示例5: 模块对比

```
问: @huppert 对比 BandPassFilter 和 WaveletFilter
答: 返回详细对比：
   - 功能差异
   - 适用场景
   - 参数对比
   - 使用建议
```

---

## 常见问题

### Q1: 提示 "@huppert 未找到"

**可能原因：**
1. Cursor 未重启
2. 配置文件路径错误
3. MCP 服务器未启动

**解决方案：**
```bash
# 1. 检查配置
cat ~/.cursor/mcp.json

# 2. 检查进程
ps aux | grep nirs_toolbox_mcp

# 3. 完全重启 Cursor
pkill -f "nirs_toolbox_mcp.py"
# Cmd+Q 退出 Cursor
# 重新打开
```

---

### Q2: 提示 "NIRS_TOOLBOX_PATH 未设置"

**解决方案：**

在 `~/.cursor/mcp.json` 中添加 `env` 字段：

```json
{
  "huppert": {
    ...
    "env": {
      "NIRS_TOOLBOX_PATH": "/你的路径/nirs-toolbox"
    }
  }
}
```

---

### Q3: Python 导入错误

**可能原因：**
- 虚拟环境未激活
- 依赖未安装

**解决方案：**
```bash
# 重新安装依赖
source venv/bin/activate
pip install -r requirements.txt

# 测试
python3 -c "from mcp.server.fastmcp import FastMCP"
```

---

### Q4: 响应很慢

**可能原因：**
- NIRS-Toolbox 文件太多
- 首次解析需要时间

**优化建议：**
- 首次查询会慢（缓存生成）
- 后续查询会快很多
- 考虑添加缓存功能（未来版本）

---

### Q5: 返回内容不完整

**可能原因：**
- MATLAB 文件格式不标准
- 注释格式特殊

**解决方案：**
- 报告问题（提供具体模块名）
- 查看原始 `.m` 文件
- 等待代码更新

---

## 进阶使用

### 自定义查询策略

#### 策略1: 从概览到细节
```
1. @huppert 有哪些预处理模块？
2. @huppert 详细介绍 OpticalDensity
3. @huppert 如何在流水线中使用它？
```

#### 策略2: 对比选择
```
1. @huppert 对比 BandPassFilter 和 WaveletFilter
2. @huppert 详细介绍 BandPassFilter
3. 根据结果选择合适的方法
```

#### 策略3: 流程构建
```
1. @huppert 预处理的标准流程
2. @huppert 详细介绍流程中的每个模块
3. 根据数据特点调整流程
```

---

### 组合使用技巧

#### 技巧1: 链式查询
```
@huppert 详细介绍 AR_IRLS
↓
了解 AR_IRLS 依赖的模块
↓
@huppert 详细介绍 nirs.design.xxxx
```

#### 技巧2: 问题驱动
```
我需要去除心跳伪迹
↓
@huppert 有哪些去伪迹的方法？
↓
@huppert 对比这些方法
↓
选择最佳方案
```

---

### 配合其他工具

#### 配合 MATLAB
```
1. 用 MCP 了解模块功能
2. 在 MATLAB 中实现代码
3. 遇到问题回到 MCP 查询
```

#### 配合文档
```
1. MCP 提供快速概览
2. 详细理论查看论文
3. 实现细节查看源码
```

---

## 📚 推荐学习路径

### 新手路径（2小时）

```
第1步（30分钟）: 安装和配置
  - 运行 setup.sh
  - 配置 Cursor
  - 测试基础功能

第2步（30分钟）: 熟悉基础查询
  - 尝试 @huppert 搜索模块
  - 尝试 @huppert 详细介绍
  - 查看不同类型的模块

第3步（30分钟）: 学习工作流
  - 查询预处理流程
  - 查询GLM分析流程
  - 理解完整流水线

第4步（30分钟）: 实战练习
  - 根据自己的需求查询
  - 对比不同方案
  - 构建自己的流程
```

---

### 进阶路径（4小时）

```
第1步: 深入理解模块
  - 详细了解每个常用模块
  - 理解参数含义
  - 掌握使用技巧

第2步: 方法对比
  - 对比不同的预处理方法
  - 对比不同的分析方法
  - 选择最适合的方案

第3步: 流程优化
  - 根据数据特点定制流程
  - 优化参数选择
  - 提高分析质量

第4步: 故障排查
  - 理解常见错误
  - 学会诊断问题
  - 掌握解决方案
```

---

## 📞 获取帮助

### 项目文档
- **快速开始**: `README.md`
- **完整指南**: `docs/NIRS_MCP_完整指南.md`
- **故障排查**: `docs/MCP问题诊断与解决.md`
- **文档索引**: `docs/DOCS_INDEX.md`

### 外部资源
- **NIRS-Toolbox**: http://huppertlab.net/nirs-toolbox/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **GitHub Issues**: （如果项目已发布）

### 社区支持
- 查看项目 Issues
- 提交 Bug 报告
- 参与讨论

---

## ✨ 使用技巧总结

### 高效查询
1. ⭐ 使用 "详细介绍" 获取完整信息
2. 🔍 先搜索，再详查
3. 📊 对比多个方案后决策
4. 🔄 查询流程时要完整的代码

### 避免的坑
1. ❌ 不要只看模块名就使用
2. ❌ 不要忽略参数说明
3. ❌ 不要跳过工作流建议
4. ❌ 不要在不理解时盲目复制代码

### 最佳实践
1. ✅ 从概览到细节
2. ✅ 对比后再选择
3. ✅ 理解参数含义
4. ✅ 参考完整示例
5. ✅ 遇到问题查文档

---

## 🎉 开始使用！

现在你已经准备好了！

**第一次尝试：**
```
@huppert 详细介绍 BandPassFilter
```

**祝使用愉快！** 🚀

---

**最后更新**: 2026-01-27  
**版本**: v1.2  
**作者**: Liam
