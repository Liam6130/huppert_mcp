#!/usr/bin/env python3
"""测试NIRS-Toolbox MCP Server"""

import subprocess
import sys
from pathlib import Path

def test_server():
    print("🧪 测试 NIRS-Toolbox MCP Server\n")
    
    server_path = Path("/Users/liam/Desktop/好用的工具/nirs_toolbox_mcp.py")
    
    # 测试 1: 检查文件存在
    print("1️⃣ 检查服务器文件...")
    if not server_path.exists():
        print(f"   ❌ 文件不存在: {server_path}")
        return False
    print(f"   ✅ 文件存在: {server_path}")
    
    # 测试 2: 检查工具箱路径
    print("\n2️⃣ 检查工具箱路径...")
    toolbox_path = Path("/Users/liam/Desktop/好用的工具/nirs-toolbox")
    if not toolbox_path.exists():
        print(f"   ❌ 工具箱路径不存在: {toolbox_path}")
        return False
    print(f"   ✅ 工具箱路径存在")
    
    # 检查关键目录
    nirs_ns = toolbox_path / "+nirs"
    demos = toolbox_path / "demos"
    
    if nirs_ns.exists():
        m_files = list(nirs_ns.rglob('*.m'))
        print(f"   ✅ +nirs 命名空间: {len(m_files)} 个.m文件")
    else:
        print(f"   ⚠️  +nirs 目录不存在")
    
    if demos.exists():
        demo_files = list(demos.glob('*.m'))
        print(f"   ✅ demos 目录: {len(demo_files)} 个示例")
    else:
        print(f"   ⚠️  demos 目录不存在")
    
    # 测试 3: 尝试导入依赖
    print("\n3️⃣ 检查依赖...")
    try:
        from mcp.server.fastmcp import FastMCP
        print("   ✅ mcp 模块已安装")
    except ImportError:
        print("   ❌ mcp 模块未安装")
        print("   请运行: pip install 'mcp[cli]'")
        return False
    
    # 测试 4: 尝试启动服务器（快速测试）
    print("\n4️⃣ 测试服务器启动...")
    try:
        proc = subprocess.Popen(
            ["python3", str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待2秒
        import time
        time.sleep(2)
        
        # 检查进程是否还在运行
        if proc.poll() is None:
            print("   ✅ 服务器启动成功")
            proc.terminate()
            proc.wait(timeout=5)
        else:
            stderr = proc.stderr.read()
            if "✅ 服务器已启动" in stderr or "工具箱路径" in stderr:
                print("   ✅ 服务器启动成功（已退出）")
            else:
                print(f"   ❌ 服务器启动失败:\n{stderr}")
                return False
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False
    
    # 测试 5: 检查Claude配置
    print("\n5️⃣ 检查 Claude Desktop 配置...")
    config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    
    if config_path.exists():
        print(f"   ✅ 配置文件存在")
        import json
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            if 'nirs-toolbox' in config.get('mcpServers', {}):
                print("   ✅ 已配置 nirs-toolbox server")
            else:
                print("   ⚠️  未配置 nirs-toolbox server")
                print("\n   请添加以下配置到 claude_desktop_config.json:")
                print('   {')
                print('     "mcpServers": {')
                print('       "nirs-toolbox": {')
                print('         "command": "python3",')
                print('         "args": [')
                print(f'           "{server_path}"')
                print('         ]')
                print('       }')
                print('     }')
                print('   }')
        except json.JSONDecodeError:
            print("   ⚠️  配置文件格式错误")
    else:
        print(f"   ⚠️  配置文件不存在: {config_path}")
        print("   请创建配置文件")
    
    print("\n" + "="*70)
    print("✅ 所有测试完成！")
    print("="*70)
    print("\n下一步:")
    print("1. 确保配置了 Claude Desktop")
    print("2. 重启 Claude Desktop (Cmd+Q)")
    print("3. 在 Claude 中测试: '查看NIRS工具箱的模块分类'")
    
    return True

if __name__ == "__main__":
    test_server()
