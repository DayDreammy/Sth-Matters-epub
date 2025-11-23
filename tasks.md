# Task List

## Pending
- [ ] **Part F: Finalize**
  - [ ] 1. Merge `refactor-core-extraction` branch into the main branch.
  - [ ] 2. Delete the `refactor-core-extraction` branch.

## In Progress
- [ ] **Part E: Commit Changes**
  - [ ] 1. Commit all refactoring changes to the `refactor-core-extraction` branch.

## Done
- [x] **Part A: 初始化与版本控制**
  - [x] 1. 创建新Git分支 `refactor-core-extraction`。
- [x] **Part B: 核心代码提取与重构**
  - [x] 1. 创建新的目录结构 (`src`, `config`, `knowledge_base`, `output`)。
  - [x] 2. 迁移、重命名并重构核心Python文件到 `src/`。
  - [x] 3. 更新所有文件内的硬编码路径和`import`语句。
- [x] **Part C: 知识库替换**
  - [x] 1. 清理旧的知识库内容。
  - [x] 2. 克隆新的知识库到 `knowledge_base/`。
- [x] **Part D: 环境与清理**
  - [x] 1. 创建 `requirements.txt`。
  - [x] 2. 更新 `.gitignore`。
  - [x] 3. 删除所有无关文件。
- [x] **Part E: 测试与验证**
  - [x] 1. 编写 `evaluate.py` 测试脚本。
  - [x] 2. 执行测试并确保生成三种格式的文档。
  - [x] 3. 成功调试并通过所有测试。
- [x] 创建 `plan.md`。
- [x] 创建 `context.md`。
- [x] 创建 `tasks.md`。
