# 📝 Changelog - huppert_mcp

所有重要的变更都会记录在这个文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [v1.2] - 2026-01-27

### 🎯 Added
- 项目重组为 `huppert_mcp` 独立项目
- 创建标准项目结构（docs/, tests/）
- 添加 `.gitignore` 文件
- 添加 `CHANGELOG.md` 版本记录
- 整理所有文档到 `docs/` 目录

### 🔧 Changed
- 更新 Cursor MCP 配置路径
- 移动虚拟环境到项目内
- 统一文档命名规范

### 📚 Documentation
- 创建项目主 README
- 整合12个文档到 docs/ 目录
- 创建文档导航索引（DOCS_INDEX.md）

---

## [v1.1] - 2026-01-27

### ✨ Added
- 新增 `get_module_details` 工具 ⭐
- 增强 `parse_matlab_class` 解析能力
- 新增 `parse_property_line` 函数
- 新增 `extract_method_comment` 函数
- 新增 `format_class_details` 格式化输出
- 新增 `suggest_related_modules` 推荐功能

### 🔧 Changed
- 改进属性解析（默认值 + 注释）
- 改进方法解析（签名 + 参数 + 注释）
- 增强输出格式（表格 + 使用示例）

### 📝 Documentation
- 创建 `AR-IRLS_Math_模块说明文档.md`
- 创建 `MCP更新日志_2026-01-27.md`
- 创建 `nirs_mcp_代码实现分析.md`

---

## [v1.0] - 2026-01-27

### 🎉 Initial Release
- MCP 服务器基础实现
- 2个 Resources（category, module）
- 3个 Tools（search_module, find_workflow, compare_modules）
- 4个 Prompts（预处理、GLM、加载、流程）

### 📚 Features
- 自动解析 MATLAB 类和函数
- 支持命名空间（+nirs）
- 提供工作流推荐
- 模块搜索和对比

### 📝 Documentation
- 创建完整实现指南
- 创建快速开始指南
- 创建使用指南

---

## 版本命名说明

- **Major（主版本）**: 重大架构变更
- **Minor（次版本）**: 新功能添加
- **Patch（补丁）**: Bug修复和小改进

当前版本：**v1.2**

---

## 未来计划

### v1.3（计划中）
- [ ] 改进 `compare_modules` 返回结构化表格
- [ ] 添加参数验证功能
- [ ] 实现模块依赖分析
- [ ] 添加缓存机制提升性能

### v2.0（愿景）
- [ ] 改为 HTTP 服务（可选）
- [ ] 添加 Web UI
- [ ] Docker 部署支持
- [ ] 多语言支持

---

**维护者**: Liam  
**更新**: 2026-01-27
