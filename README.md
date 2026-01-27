# 🧠 Huppert MCP - NIRS Toolbox Assistant

**版本**: v1.2  
**更新**: 2026-01-27

NIRS-Toolbox 的 MCP (Model Context Protocol) 服务器，让 AI 助手能直接查阅 fNIRS 数据分析工具文档。

---

## ⚡ 快速开始

### 前置要求
- Python 3.10+
- Cursor IDE
- NIRS-Toolbox 完整代码

### 安装步骤

```bash
# 1. 进入项目目录
cd huppert_mcp

# 2. 运行安装脚本
./setup.sh

# 会提示输入 NIRS-Toolbox 路径
# 自动完成：虚拟环境创建、依赖安装、配置生成
```

### 配置 Cursor

打开 `~/.cursor/mcp.json`，添加生成的配置：

```json
{
  "mcpServers": {
    "huppert": {
      "name": "Huppert Lab NIRS Toolbox",
      "command": "/完整路径/huppert_mcp/venv/bin/python3",
      "args": ["/完整路径/huppert_mcp/nirs_toolbox_mcp.py"],
      "env": {
        "NIRS_TOOLBOX_PATH": "/完整路径/nirs-toolbox"
      }
    }
  }
}
```

### 测试

```
1. Cmd+Q 退出 Cursor
2. 重新打开 Cursor
3. 输入: @huppert 详细介绍 BandPassFilter
```

---

## 🎯 主要功能

### Resources（资源）
- `category://` - 列出所有模块类别
- `module://` - 查看特定模块详情
- `demo://` - 获取示例代码

### Tools（工具）
- `search_module` - 搜索模块
- `get_module_details` ⭐ - 获取完整模块信息（属性、方法、示例）
- `find_workflow` - 查找工作流推荐
- `compare_modules` - 对比模块差异

### Prompts（提示）
- `how_to_preprocess` - 预处理指南
- `how_to_glm_analysis` - GLM分析指南
- `how_to_load_data` - 数据加载指南
- `build_pipeline` - 构建流水线

---

## 💻 使用示例

### 基础查询
```
@huppert BandPassFilter
@huppert 有哪些滤波模块？
```

### 详细查询（推荐）
```
@huppert 详细介绍 AR_IRLS
@huppert 详细介绍 BeerLambertLaw
```

### 工作流推荐
```
@huppert 预处理的标准流程是什么？
@huppert 如何进行GLM分析？
```

### 模块对比
```
@huppert 对比 BandPassFilter 和 WaveletFilter
```

---

## 📚 文档

- **快速开始**: `START_HERE.md`
- **用户指南**: `docs/USER_GUIDE.md` ⭐
- **完整教程**: `docs/NIRS_MCP_完整指南.md`
- **故障排查**: `docs/MCP问题诊断与解决.md`
- **所有文档**: `docs/DOCS_INDEX.md`

---

## 🐛 故障排查

### 问题：@huppert 未找到

```bash
# 1. 检查配置
cat ~/.cursor/mcp.json

# 2. 检查进程
ps aux | grep nirs_toolbox_mcp

# 3. 重启 Cursor
pkill -f "nirs_toolbox_mcp.py"
# Cmd+Q 退出，重新打开
```

### 问题：NIRS_TOOLBOX_PATH 未设置

在 `~/.cursor/mcp.json` 中添加 `env` 字段：

```json
"env": {
  "NIRS_TOOLBOX_PATH": "/你的路径/nirs-toolbox"
}
```

更多问题查看 `docs/MCP问题诊断与解决.md`

---

## 📦 项目结构

```
huppert_mcp/
├── nirs_toolbox_mcp.py       # MCP服务器主程序
├── setup.sh                  # 自动安装脚本
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明
├── CHANGELOG.md              # 版本历史
├── LICENSE                   # MIT许可证
│
├── docs/                     # 文档目录
│   ├── USER_GUIDE.md         # 用户指南 ⭐
│   ├── NIRS_MCP_完整指南.md   # 完整教程
│   ├── NIRS_MCP_快速入门.md   # 快速入门
│   └── MCP问题诊断与解决.md   # 故障排查
│
└── tests/                    # 测试目录
    └── test_nirs_mcp.py
```

---

## 🔗 相关链接

- **NIRS-Toolbox**: http://huppertlab.net/nirs-toolbox/
- **GitHub**: https://github.com/huppertt/nirs-toolbox
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Huppert Lab**: http://huppertlab.net/

---

## 📝 许可证

MIT License - 详见 `LICENSE` 文件

本项目提供 NIRS-Toolbox 的 MCP 接口，NIRS-Toolbox 本身有其独立的许可证。

---

## 🙏 致谢

- **Theodore J. Huppert 教授** - NIRS-Toolbox 创始人
- **Huppert Lab** - 工具箱开发团队
- **MCP 社区** - 协议开发者

---

**让 fNIRS 数据分析更简单！** 🚀

**作者**: Liam  
**版本**: v1.2  
**更新**: 2026-01-27
