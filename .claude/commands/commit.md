# Git Commit Workflow

执行完整的Git提交流程，包括状态检查、差异查看、文件暂存、提交和推送。

## 执行步骤

1. **检查Git状态** - 运行 `git status` 查看当前修改的文件
2. **查看差异** - 运行 `git diff` 检查具体的修改内容
3. **暂存文件** - 使用 `git add <files>` 暂存相关文件（切勿使用 `git add .`）
4. **创建提交** - 运行 `git commit -m` 创建描述性提交信息
5. **推送到远程** - 运行 `git push` 将提交推送到远程仓库

## 注意事项

- **切勿使用** `git add .` 命令
- **仔细检查** 每个修改的文件内容
- **创建描述性** 的提交信息，说明修改的目的和内容
- **确保** 只提交相关的修改文件

## 示例提交信息格式

```
feat: add new feature description
fix: resolve specific issue
docs: update documentation
refactor: improve code structure
```

## 推送前检查

在推送之前，确认：
- 所有相关文件已正确暂存
- 提交信息清晰描述了修改内容
- 没有意外包含不相关的文件