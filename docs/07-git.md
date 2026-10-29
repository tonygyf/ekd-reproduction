# Git 与公开仓库

根目录为复现仓库，EKD/ 为固定到作者提交的子模块。补丁单独版本控制，避免在复现仓库中复制上游全部历史和下载文件。

- .gitignore：排除数据、权重、checkpoint、PDF、原始日志、缓存、.env 和本地密钥。
- .gitattributes / .editorconfig：统一文本换行，PNG 作为二进制。
- patches/upstream-fixes.patch：本轮最小修复。
- scripts/prepare_source.sh：初始化子模块并应用补丁，重复执行会确认已应用，不会重置本地修改。
- results/：可公开的结构化验证结果与最终报告；完整机器日志保留在本地 logs/。
- 提交身份使用 GitHub noreply 地址。

补丁应用后子模块显示已修改是预期状态；子模块引用仍固定原始官方提交。

## 远端发布

公开仓库：https://github.com/tonygyf/ekd-reproduction

用户在 GitHub 网页创建空 public 仓库，本机 SSH key 已认证为 tonygyf，origin 使用 `git@github.com:tonygyf/ekd-reproduction.git`。推送无需 GitHub CLI 登录。

```bash
git push -u origin main
```

SSH 认证负责推送；创建新仓库需网页或 GitHub API。本机无需为本次发布另存 API token。
