# 📦 GitHub Repository Rename Guide

## 目标

将仓库从 `agent-usdc-faucet` 重命名为 `agent-liquidity-nexus`

---

## 🔄 GitHub 重命名步骤

### 1. 在 GitHub 上重命名仓库

1. 打开仓库页面:
   ```
   https://github.com/csschan/agent-usdc-faucet
   ```

2. 点击 **Settings** (设置)

3. 在 "Repository name" 部分:
   - 当前名称: `agent-usdc-faucet`
   - 新名称: `agent-liquidity-nexus`

4. 点击 **Rename** 按钮

5. GitHub 会自动设置重定向（旧链接仍然有效）

---

## 💻 本地更新步骤

### 重命名后更新本地仓库

```bash
# 1. 更新远程 URL
cd /Users/css/Desktop/privalert/agent-usdc-faucet
git remote set-url origin https://github.com/csschan/agent-liquidity-nexus.git

# 2. 验证新 URL
git remote -v

# 3. 拉取确认
git pull

# 4. 重命名本地文件夹（可选）
cd /Users/css/Desktop/privalert
mv agent-usdc-faucet agent-liquidity-nexus
cd agent-liquidity-nexus
```

---

## 📝 需要更新的外部链接

### 1. Moltbook 提交
更新帖子中的 GitHub 链接:
```
旧: https://github.com/csschan/agent-usdc-faucet
新: https://github.com/csschan/agent-liquidity-nexus
```

### 2. README.md 中的链接
已自动更新（在同一仓库内）

### 3. Railway 部署
Railway 会自动跟随 GitHub 仓库重命名，无需手动更新

---

## ✅ 验证清单

重命名完成后验证：

- [ ] GitHub 仓库 URL 已更改
- [ ] 旧 URL 重定向到新 URL
- [ ] 本地 git remote 已更新
- [ ] Moltbook 链接已更新
- [ ] Railway 部署正常工作
- [ ] README 中的所有链接正常

---

## 🔗 新链接

重命名后:

**GitHub**: https://github.com/csschan/agent-liquidity-nexus
**API**: https://charismatic-simplicity-production-1854.up.railway.app
**Moltbook**: https://www.moltbook.com/post/b021cdea-de86-4460-8c4b-8539842423fe

---

## ⚠️ 注意事项

### GitHub 自动重定向
- ✅ GitHub 会自动设置 301 重定向
- ✅ 旧链接仍然有效（至少 1 年）
- ✅ git clone/pull 仍然工作

### 不需要担心
- ❌ 不会丢失 stars
- ❌ 不会丢失 forks
- ❌ 不会丢失 issues
- ❌ 不会影响 git history

---

## 📊 影响评估

### ✅ 无影响
- Git commit history
- GitHub stars/forks
- Railway 部署
- API 端点
- 智能合约地址

### ⚠️ 需要更新
- Moltbook 帖子中的链接
- 个人书签
- 外部文档引用

---

## 🚀 重命名后的好处

1. **品牌一致性**
   ```
   项目名称 = GitHub 仓库名称
   Agent Liquidity Nexus = agent-liquidity-nexus
   ```

2. **专业形象**
   ```
   旧: agent-usdc-faucet (工具感)
   新: agent-liquidity-nexus (基础设施感)
   ```

3. **更好的 SEO**
   - "liquidity nexus" 更容易被搜索到
   - 体现核心价值主张

---

## 📞 需要帮助？

如果遇到问题：
1. GitHub 重定向会处理大部分情况
2. 本地只需更新 remote URL
3. Railway 会自动跟随

---

**准备好重命名了吗？**

只需在 GitHub Settings 中点击几下即可！🎯
