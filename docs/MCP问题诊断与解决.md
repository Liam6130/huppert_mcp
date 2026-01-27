# 🔧 NIRS MCP 问题诊断与解决方案

**诊断日期**: 2026-01-27  
**问题**: NIRS MCP 无法像 Langchain 一样调用；重启Cursor后仍提示未重启
**更新**: 已改名为 @huppert

---

## 🔴 问题1: 进程状态异常

### 发现的问题

```bash
# 当前运行的MCP进程
PID 6465: /opt/homebrew/.../Python /Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py
PID 6394: /opt/homebrew/.../Python /Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py

# 问题：
# 1. 有两个进程在运行（应该只有1个）
# 2. 使用的是系统Python，不是虚拟环境的Python
```

### 配置vs实际运行

| 项目 | 配置文件 | 实际运行 | 状态 |
|------|---------|---------|------|
| **Python路径** | `/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3` | `/opt/homebrew/.../Python` | ❌ 不一致 |
| **进程数量** | 1个 | 2个 | ❌ 异常 |
| **启动方式** | stdio | stdio | ✅ 正确 |

---

## 🔴 问题2: 与Langchain MCP的对比

### Langchain vs. huppert

| 特性 | Langchain MCP | huppert MCP |
|------|--------------|--------------|
| **类型** | 远程HTTP服务 | 本地Python脚本 |
| **配置** | `"url": "https://..."` | `"command": "python3 ..."` |
| **启动方式** | Cursor调用远程API | Cursor启动本地进程 |
| **通信方式** | HTTP请求/响应 | stdio (标准输入/输出) |
| **依赖** | 无需本地安装 | 需要虚拟环境 |
| **Resources** | ✅ 有 | ✅ 有 |
| **Tools** | ✅ 有 | ✅ 有 |
| **Prompts** | ✅ 有 | ✅ 有 |

### 为什么感觉"不能调用"？

**实际情况**: huppert **已经可以调用**！只是方式不同：

```
Langchain: @Docs by LangChain 搜索文档
           ↓
           HTTP API调用
           ↓
           返回结果

huppert:  @huppert 查询模块
           ↓
           本地进程通信（stdio）
           ↓
           返回结果
```

**关键区别**: 
- Langchain是**云端服务**，不需要担心进程状态
- huppert是**本地服务**，需要确保进程正常运行

---

## 🔴 问题3: 为什么重启后仍提示未重启？

### 可能的原因

#### 原因1: 旧进程未完全杀死 ⭐⭐⭐⭐⭐

```bash
# 发现：有2个进程在运行
PID 6465 和 PID 6394

# 推测：
# 1. 第一次启动时创建了进程 6394
# 2. 重启Cursor时创建了新进程 6465
# 3. 但旧进程 6394 没有被杀死
# 4. Cursor可能在使用旧进程（缓存的连接）
```

#### 原因2: Python解释器路径错误 ⭐⭐⭐⭐

```json
// mcp.json 中配置
"command": "/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3"

// 实际运行的
/opt/homebrew/Cellar/python@3.14/.../Python

// 说明：Cursor可能缓存了旧的启动命令
```

#### 原因3: Cursor缓存机制 ⭐⭐⭐

Cursor可能会：
- 缓存MCP服务器的元数据
- 缓存工具描述（tools/）
- 缓存资源描述（resources/）
- 缓存提示描述（prompts/）

即使重启，缓存可能仍然存在。

---

## ✅ 解决方案

### 方案1: 彻底清理并重启 ⭐⭐⭐⭐⭐ (推荐)

```bash
# Step 1: 杀死所有MCP进程
pkill -f "nirs_toolbox_mcp.py"

# Step 2: 验证进程已被杀死
ps aux | grep nirs_toolbox_mcp | grep -v grep
# 应该没有输出

# Step 3: 清理Cursor缓存（可选但推荐）
rm -rf ~/.cursor/projects/Users-liam-Desktop/mcps/user-huppert/*
# 注意：这会删除缓存的工具描述，Cursor会重新生成

# Step 4: 完全退出Cursor
# macOS: Cmd+Q（不是关闭窗口！）
# 或者：killall Cursor

# Step 5: 等待10秒

# Step 6: 重新打开Cursor

# Step 7: 测试
# 在Chat中输入：@huppert
# 应该能看到服务器列表
```

### 方案2: 修正Python路径并重启 ⭐⭐⭐⭐

**问题诊断**:
```bash
# 检查虚拟环境的Python是否存在
ls -la /Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3

# 如果存在，检查是否可执行
/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3 --version

# 如果不存在或报错，说明虚拟环境有问题
```

**解决方法**:
```bash
# 方案A: 修复虚拟环境
cd /Users/liam/Desktop/好用的工具
source nirs_mcp_env/bin/activate
pip install --upgrade "mcp[cli]"

# 方案B: 重建虚拟环境
cd /Users/liam/Desktop/好用的工具
rm -rf nirs_mcp_env
python3 -m venv nirs_mcp_env
source nirs_mcp_env/bin/activate
pip install "mcp[cli]"
```

### 方案3: 临时使用系统Python ⭐⭐ (快速测试)

```json
// 修改 ~/.cursor/mcp.json
{
  "mcpServers": {
    "huppert": {
      "name": "fNIRS Toolbox",
      "command": "python3",  // 改用系统Python
      "args": [
        "/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/opt/homebrew/lib/python3.14/site-packages"
      }
    }
  }
}
```

**注意**: 这要求系统Python已安装`mcp`包：
```bash
pip3 install "mcp[cli]"
```

---

## 🧪 测试与验证

### 测试1: 检查进程状态

```bash
# 1. 启动Cursor后，检查进程
ps aux | grep nirs_toolbox_mcp | grep -v grep

# 期望结果：只有1个进程
# liam  12345  ... /Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3 ...

# 2. 检查进程使用的Python
ps aux | grep nirs_toolbox_mcp | grep -v grep | awk '{print $11}'

# 期望结果：
# /Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3
```

### 测试2: 测试MCP功能

在Cursor Chat中依次测试：

```
1. 测试服务器连接
   输入: @huppert
   期望: 看到服务器名称

2. 测试Resource
   输入: @huppert 列出所有类别
   期望: AI调用 list_categories 并返回结果

3. 测试Tool
   输入: @huppert 搜索 BandPassFilter
   期望: AI调用 search_module 并返回结果

4. 测试新功能 (get_module_details)
   输入: @huppert 详细介绍 BandPassFilter
   期望: 返回完整的属性表格、方法列表、使用示例

5. 测试Prompt
   输入: @huppert 帮我预处理数据
   期望: AI使用 how_to_preprocess 提示模板
```

### 测试3: 检查MCP日志

```bash
# Cursor的MCP日志位置
tail -f ~/Library/Logs/Cursor/main.log | grep -i mcp

# 或者查看Python脚本的stderr输出
# （如果启动了终端，会看到）
```

---

## 📊 对比表：三种MCP类型

| 特性 | 远程HTTP (Langchain) | 本地stdio (huppert) | 本地HTTP (可选) |
|------|---------------------|---------------------|-----------------|
| **配置** | `"url": "..."` | `"command": "..."` | `"url": "http://localhost:..."` |
| **依赖** | 无 | Python虚拟环境 | Python虚拟环境 |
| **启动** | 自动（远程） | Cursor启动 | 手动启动 |
| **调试** | 难（远程） | 中等（本地） | 易（浏览器） |
| **性能** | 网络延迟 | 最快 | 中等 |
| **可靠性** | 依赖网络 | 依赖进程 | 依赖进程 |

---

## 💡 改进建议

### 短期改进（立即可行）

1. **添加健康检查**
   ```python
   # 在 nirs_toolbox_mcp.py 中添加
   @mcp.tool()
   def health_check() -> str:
       """检查MCP服务器健康状态"""
       return f"✅ huppert MCP服务器运行正常\n版本: v1.1\n进程ID: {os.getpid()}"
   ```

2. **添加日志输出**
   ```python
   # 在文件开头添加
   import logging
   logging.basicConfig(
       filename='/Users/liam/Desktop/好用的工具/mcp_debug.log',
       level=logging.INFO,
       format='%(asctime)s - %(message)s'
   )
   
   # 在关键位置添加
   logging.info(f"MCP服务器启动，PID: {os.getpid()}")
   logging.info(f"工具箱路径: {NIRS_TOOLBOX_PATH}")
   ```

3. **优化启动脚本**
   ```bash
   #!/bin/bash
   # 文件: /Users/liam/Desktop/好用的工具/start_mcp.sh
   
   # 清理旧进程
   pkill -f "nirs_toolbox_mcp.py"
   
   # 启动新进程
   source /Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/activate
   python /Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py
   ```

### 长期改进（可选）

1. **改为HTTP服务**（类似Langchain）
   ```python
   # 使用 FastMCP 的HTTP传输层
   from mcp.server.fastmcp import FastMCP
   
   mcp = FastMCP("huppert")
   
   if __name__ == "__main__":
       mcp.run(transport="http", port=8080)
   ```
   
   配置：
   ```json
   {
     "huppert": {
       "url": "http://localhost:8080/mcp"
     }
   }
   ```

2. **Docker化部署**
   ```dockerfile
   FROM python:3.10
   COPY . /app
   WORKDIR /app
   RUN pip install "mcp[cli]"
   CMD ["python", "nirs_toolbox_mcp.py"]
   ```

---

## 🎯 立即执行的步骤

### 现在马上做（5分钟）

```bash
# 1. 打开终端

# 2. 杀死所有MCP进程
pkill -f "nirs_toolbox_mcp.py"

# 3. 验证
ps aux | grep nirs_toolbox_mcp | grep -v grep
# 应该没有输出

# 4. 完全退出Cursor（重要！）
# macOS: Cmd+Q
# 或者：killall Cursor

# 5. 等待10秒

# 6. 重新打开Cursor

# 7. 测试
# 在Chat中输入：@huppert health_check
# 如果看到错误，继续下一步

# 8. 如果仍然有问题，检查虚拟环境
cd /Users/liam/Desktop/好用的工具
source nirs_mcp_env/bin/activate
python -c "from mcp.server.fastmcp import FastMCP; print('✅ MCP安装正常')"

# 如果报错，重新安装
pip install --force-reinstall "mcp[cli]"
```

---

## 📞 如果问题仍然存在

### 收集诊断信息

```bash
# 1. 检查Cursor配置
cat ~/.cursor/mcp.json

# 2. 检查Python环境
which python3
/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3 --version

# 3. 检查MCP安装
/Users/liam/Desktop/好用的工具/nirs_mcp_env/bin/python3 -c "import mcp; print(mcp.__version__)"

# 4. 检查进程
ps aux | grep nirs_toolbox_mcp

# 5. 检查MCP缓存
ls -la ~/.cursor/projects/Users-liam-Desktop/mcps/user-huppert/

# 6. 测试直接运行
cd /Users/liam/Desktop/好用的工具
source nirs_mcp_env/bin/activate
python nirs_toolbox_mcp.py
# 应该看到启动信息，然后等待输入
```

---

## 📚 总结

### 核心问题

1. ✅ **huppert MCP 本身没问题** - Resources、Tools、Prompts都有
2. ❌ **进程管理有问题** - 多个进程、Python路径错误
3. ❌ **缓存问题** - Cursor可能使用旧的连接

### 解决方案优先级

1. **首选**: 彻底清理进程 + 重启Cursor
2. **备选**: 修复虚拟环境Python路径
3. **快速**: 临时使用系统Python

### 与Langchain的差异

| Langchain | huppert |
|-----------|----------|
| 云端服务，无需担心进程 | 本地服务，需要管理进程 |
| 通过HTTP调用 | 通过stdio通信 |
| 配置简单（只需URL） | 配置复杂（需要Python环境） |
| **功能一样** | **功能一样** |

**结论**: huppert MCP **可以像Langchain一样调用**，只是底层通信方式不同。问题在于进程管理，不是MCP功能本身！

---

**下一步**: 立即执行"立即执行的步骤"，然后测试 `@huppert` 是否工作！

Good luck! 🚀
