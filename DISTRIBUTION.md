# 📦 分发说明

## 快速分发

### 方式1: GitHub（推荐）

```bash
cd huppert_mcp_dist
git init
git add .
git commit -m "Release v1.2"
git remote add origin https://github.com/your-username/huppert_mcp.git
git push -u origin main
```

### 方式2: 打包

```bash
cd huppert_mcp_dist
./package.sh
# 生成 huppert_mcp_v1.2.tar.gz
```

---

## 接收者使用

```bash
# Git方式
git clone <repo-url>
cd huppert_mcp
./setup.sh

# 压缩包方式
tar -xzf huppert_mcp_v1.2.tar.gz
cd huppert_mcp_v1.2
./setup.sh
```

---

## 文件说明

### 核心文件
- `nirs_toolbox_mcp.py` - MCP服务器
- `setup.sh` - 自动安装脚本
- `requirements.txt` - 依赖清单

### 文档文件
- `README.md` - 项目说明
- `docs/USER_GUIDE.md` - 用户指南
- `docs/NIRS_MCP_完整指南.md` - 完整教程

### 配置文件
- `LICENSE` - MIT许可证
- `.gitignore` - Git忽略规则

---

**分发包大小**: ~680KB  
**安装时间**: ~15分钟
