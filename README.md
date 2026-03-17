# CogniCore - 完整类人认知核心

CogniCore 是一个完整的类人认知架构实现，提供记忆存储、持续学习、问题解决和工具集成的全套功能。

## 📦 功能特性

- **四层记忆系统**：工作记忆、情景记忆、语义记忆、程序性记忆
- **智能检索系统**：SQLite FTS5 全文搜索
- **学习机制**：自动检测用户纠正和功能请求
- **问题解决框架**：模式匹配、任务分解、多Agent协作
- **工具集成**：Skills as Tools、Auto-discovery、Tool Chaining

## 🛠️ 安装使用

```bash
# 克隆仓库
git clone https://github.com/talktoto/cognicore.git

# 复制到 OpenClaw 技能目录
cp -r cognicore ~/.openclaw/skills/

# 或直接下载 SKILL.md
curl -L https://raw.githubusercontent.com/talktoto/cognicore/master/SKILL.md -o ~/.openclaw/skills/cognicore/SKILL.md
```

## 📝 使用说明

- **记录记忆**：直接说"记住..."或相关重要信息
- **触发学习**：纠正错误或提出新需求  
- **查询记忆**：询问相关历史信息
- **复杂任务**：系统自动规划多Agent协作

## 📄 许可证

MIT License - 允许商业使用、修改、分发和私有化。

---

**CogniCore - 完整的类人认知解决方案**
