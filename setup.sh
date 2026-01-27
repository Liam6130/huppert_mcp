#!/bin/bash

# ============================================
# Huppert MCP Server - 安装脚本
# ============================================

set -e  # 遇到错误立即退出

echo "🚀 开始安装 Huppert MCP Server..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================
# 1. 检查 Python 版本
# ============================================
echo "📍 Step 1: 检查 Python 环境..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 python3${NC}"
    echo "请先安装 Python 3.10 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python 版本: $(python3 --version)${NC}"

# ============================================
# 2. 检查 NIRS-Toolbox 路径
# ============================================
echo ""
echo "📍 Step 2: 配置 NIRS-Toolbox 路径..."

if [ -z "$NIRS_TOOLBOX_PATH" ]; then
    echo -e "${YELLOW}⚠️  未设置 NIRS_TOOLBOX_PATH 环境变量${NC}"
    echo ""
    read -p "请输入 NIRS-Toolbox 完整路径: " NIRS_TOOLBOX_PATH
    
    if [ ! -d "$NIRS_TOOLBOX_PATH" ]; then
        echo -e "${RED}❌ 错误：路径不存在: $NIRS_TOOLBOX_PATH${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ NIRS-Toolbox 路径: $NIRS_TOOLBOX_PATH${NC}"

# 验证关键目录
if [ ! -d "$NIRS_TOOLBOX_PATH/+nirs" ]; then
    echo -e "${RED}❌ 错误：未找到 +nirs 目录${NC}"
    echo "请确认这是正确的 NIRS-Toolbox 路径"
    exit 1
fi

# ============================================
# 3. 创建虚拟环境
# ============================================
echo ""
echo "📍 Step 3: 创建 Python 虚拟环境..."

if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  虚拟环境已存在，跳过创建${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✅ 虚拟环境创建成功${NC}"
fi

# ============================================
# 4. 安装依赖
# ============================================
echo ""
echo "📍 Step 4: 安装 Python 依赖..."

source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${GREEN}✅ 依赖安装完成${NC}"

# 验证安装
if python3 -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null; then
    echo -e "${GREEN}✅ MCP 模块验证通过${NC}"
else
    echo -e "${RED}❌ MCP 模块安装失败${NC}"
    exit 1
fi

# ============================================
# 5. 创建配置文件
# ============================================
echo ""
echo "📍 Step 5: 生成配置文件..."

cat > config.json <<EOF
{
  "nirs_toolbox_path": "$NIRS_TOOLBOX_PATH",
  "mcp_name": "huppert",
  "mcp_display_name": "Huppert Lab NIRS Toolbox"
}
EOF

echo -e "${GREEN}✅ 配置文件已创建: config.json${NC}"

# ============================================
# 6. 测试运行
# ============================================
echo ""
echo "📍 Step 6: 测试 MCP 服务器..."

# 导出环境变量
export NIRS_TOOLBOX_PATH="$NIRS_TOOLBOX_PATH"

# 测试导入
if python3 -c "import sys; sys.path.insert(0, '.'); from nirs_toolbox_mcp import mcp" 2>/dev/null; then
    echo -e "${GREEN}✅ MCP 服务器测试通过${NC}"
else
    echo -e "${YELLOW}⚠️  MCP 服务器导入测试失败（可能正常，需要在 Cursor 中运行）${NC}"
fi

# ============================================
# 7. 生成 Cursor 配置
# ============================================
echo ""
echo "📍 Step 7: 生成 Cursor MCP 配置..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python3"
SERVER_PATH="$SCRIPT_DIR/nirs_toolbox_mcp.py"

cat > cursor_mcp_config.json <<EOF
{
  "mcpServers": {
    "huppert": {
      "name": "Huppert Lab NIRS Toolbox",
      "command": "$PYTHON_PATH",
      "args": ["$SERVER_PATH"],
      "env": {
        "NIRS_TOOLBOX_PATH": "$NIRS_TOOLBOX_PATH"
      }
    }
  }
}
EOF

echo -e "${GREEN}✅ Cursor 配置已生成: cursor_mcp_config.json${NC}"

# ============================================
# 8. 完成提示
# ============================================
echo ""
echo "============================================"
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "============================================"
echo ""
echo "📝 下一步操作："
echo ""
echo "1️⃣  配置 Cursor"
echo "   打开: ~/.cursor/mcp.json"
echo "   添加以下内容:"
echo ""
cat cursor_mcp_config.json
echo ""
echo "2️⃣  重启 Cursor"
echo "   - Cmd+Q 完全退出"
echo "   - 重新打开 Cursor"
echo ""
echo "3️⃣  测试功能"
echo "   在 Cursor Chat 中输入:"
echo "   @huppert 详细介绍 BandPassFilter"
echo ""
echo "============================================"
echo ""
echo "📚 文档位置:"
echo "   - 用户指南: docs/USER_GUIDE.md"
echo "   - 完整文档: docs/DOCS_INDEX.md"
echo ""
echo "❓ 遇到问题？查看: docs/MCP问题诊断与解决.md"
echo ""
echo "✨ 祝使用愉快！"
echo ""

deactivate 2>/dev/null || true
