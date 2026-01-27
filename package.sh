#!/bin/bash

# ============================================
# Huppert MCP - 打包脚本
# 用于创建可分发的压缩包
# ============================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📦 开始打包 Huppert MCP..."
echo ""

# 获取版本号
VERSION=$(grep "版本" README.md | head -1 | grep -o 'v[0-9.]*' || echo "v1.2")
PACKAGE_NAME="huppert_mcp_${VERSION}"

echo "版本: $VERSION"
echo "包名: $PACKAGE_NAME.tar.gz"
echo ""

# ============================================
# 1. 清理临时文件
# ============================================
echo "📍 Step 1: 清理临时文件..."

rm -rf venv nirs_mcp_env 2>/dev/null || true
rm -rf __pycache__ */__pycache__ 2>/dev/null || true
rm -f *.pyc */*.pyc 2>/dev/null || true
rm -f config.json cursor_mcp_config.json 2>/dev/null || true

echo -e "${GREEN}✅ 清理完成${NC}"

# ============================================
# 2. 创建文件列表
# ============================================
echo ""
echo "📍 Step 2: 准备打包文件..."

FILES=(
    "nirs_toolbox_mcp.py"
    "requirements.txt"
    "setup.sh"
    "package.sh"
    "README.md"
    "CHANGELOG.md"
    "DISTRIBUTION.md"
    "PROJECT_STATUS.md"
    "LICENSE"
    "START_HERE.md"
    ".gitignore"
    "docs/"
    "tests/"
)

# 验证关键文件存在
for file in "nirs_toolbox_mcp.py" "requirements.txt" "setup.sh" "README.md"; do
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}❌ 错误：缺少关键文件 $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ 文件检查通过${NC}"

# ============================================
# 3. 创建临时目录
# ============================================
echo ""
echo "📍 Step 3: 创建打包结构..."

TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/$PACKAGE_NAME"

# 复制文件
cp -r "${FILES[@]}" "$TEMP_DIR/$PACKAGE_NAME/" 2>/dev/null || true

echo -e "${GREEN}✅ 文件复制完成${NC}"

# ============================================
# 4. 创建压缩包
# ============================================
echo ""
echo "📍 Step 4: 创建压缩包..."

cd "$TEMP_DIR"
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME"

# 移动到项目目录
mv "$PACKAGE_NAME.tar.gz" "$OLDPWD/"

cd "$OLDPWD"

# 清理临时目录
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✅ 压缩包创建完成${NC}"

# ============================================
# 5. 生成校验和
# ============================================
echo ""
echo "📍 Step 5: 生成校验和..."

if command -v shasum &> /dev/null; then
    shasum -a 256 "$PACKAGE_NAME.tar.gz" > "$PACKAGE_NAME.tar.gz.sha256"
    echo -e "${GREEN}✅ SHA256 校验和已生成${NC}"
elif command -v sha256sum &> /dev/null; then
    sha256sum "$PACKAGE_NAME.tar.gz" > "$PACKAGE_NAME.tar.gz.sha256"
    echo -e "${GREEN}✅ SHA256 校验和已生成${NC}"
else
    echo -e "${YELLOW}⚠️  未找到 shasum/sha256sum，跳过校验和生成${NC}"
fi

# ============================================
# 6. 统计信息
# ============================================
echo ""
echo "============================================"
echo -e "${GREEN}🎉 打包完成！${NC}"
echo "============================================"
echo ""

PACKAGE_SIZE=$(du -h "$PACKAGE_NAME.tar.gz" | cut -f1)

echo "📦 分发包信息:"
echo "   文件名: $PACKAGE_NAME.tar.gz"
echo "   大小: $PACKAGE_SIZE"
echo ""

if [ -f "$PACKAGE_NAME.tar.gz.sha256" ]; then
    echo "🔒 校验和:"
    cat "$PACKAGE_NAME.tar.gz.sha256"
    echo ""
fi

echo "📝 包含内容:"
tar -tzf "$PACKAGE_NAME.tar.gz" | head -20
if [ $(tar -tzf "$PACKAGE_NAME.tar.gz" | wc -l) -gt 20 ]; then
    echo "   ... ($(tar -tzf "$PACKAGE_NAME.tar.gz" | wc -l) 个文件)"
fi
echo ""

# ============================================
# 7. 使用说明
# ============================================
echo "============================================"
echo "📤 分发说明:"
echo "============================================"
echo ""
echo "1️⃣  分发文件:"
echo "   $PACKAGE_NAME.tar.gz"
echo ""
echo "2️⃣  接收者解压:"
echo "   tar -xzf $PACKAGE_NAME.tar.gz"
echo "   cd $PACKAGE_NAME"
echo "   ./setup.sh"
echo ""
echo "3️⃣  详细说明:"
echo "   - 用户指南: docs/USER_GUIDE.md"
echo "   - 快速开始: START_HERE.md"
echo ""
echo "✨ 祝分发顺利！"
echo ""
