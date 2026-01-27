# 🚀 开始使用 Huppert MCP

**欢迎！** 👋

这是 NIRS-Toolbox 的 MCP (Model Context Protocol) 服务器，让 AI 助手能直接查阅 fNIRS 数据分析工具的文档。

---

## ⚡ 快速开始（3步）

### Step 1: 运行安装脚本

```bash
cd huppert_mcp
./setup.sh
```

**会提示你输入 NIRS-Toolbox 路径**

---

### Step 2: 配置 Cursor

```bash
# 打开配置文件
open ~/.cursor/mcp.json

# 复制 cursor_mcp_config.json 的内容到里面
```

---

### Step 3: 测试

```
1. 重启 Cursor (Cmd+Q)
2. 打开 Cursor
3. 输入: @huppert 详细介绍 BandPassFilter
```

**成功！** ✅

---

## 📚 详细文档

- **首次使用？** → `docs/USER_GUIDE.md` ⭐
- **快速了解？** → `README.md`
- **遇到问题？** → `docs/MCP问题诊断与解决.md`
- **所有文档？** → `docs/DOCS_INDEX.md`

---

## ❓ 常见问题

**Q: 安装需要多久？**  
A: 约10-15分钟

**Q: 需要什么？**  
A: Python 3.10+, Cursor IDE, NIRS-Toolbox

**Q: 出错了怎么办？**  
A: 查看 `docs/MCP问题诊断与解决.md`

---

## 🎯 主要功能

- 🔍 搜索模块
- 📖 查看完整文档
- 🔄 工作流推荐
- ⚖️ 模块对比

---

## 💡 使用示例

```
@huppert BandPassFilter
@huppert 详细介绍 AR_IRLS
@huppert 有哪些滤波模块？
@huppert 预处理的标准流程是什么？
```

---

**祝使用愉快！** 🎉

有问题查看 `docs/USER_GUIDE.md` 或 `docs/DOCS_INDEX.md`
