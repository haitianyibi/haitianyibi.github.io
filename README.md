# 我的个人笔记网站

这是一个基于 Jekyll 和 GitHub Pages 的个人笔记网站。网站包含技术笔记、学习总结和实践经验等内容。

## 网站结构

- `_posts/` - 存放笔记文章，按日期自动排序
- `doc/` - 存放文档和参考资料
- `_layouts/` - 自定义页面布局
- `assets/` - 存放 CSS、JS 等静态资源
- `notes.md` - 所有笔记列表页面
- `categories.md` - 按分类浏览笔记页面
- `about.md` - 关于页面

## 如何添加新笔记

1. 在 `_posts` 目录下创建新的 Markdown 文件，文件名格式为 `YYYY-MM-DD-标题.md`
2. 在文件开头添加 front matter 配置：

```markdown
---
layout: post
title: "笔记标题"
date: YYYY-MM-DD HH:MM:SS
tags: [标签1, 标签2]
---
```

3. 在 front matter 下面编写笔记内容

## 本地预览

如果您想在本地预览网站：

1. 确保系统已安装 Ruby 和 Jekyll
2. 在项目根目录运行 `bundle install`
3. 运行 `bundle exec jekyll serve`
4. 访问 `http://localhost:4000` 预览网站

## 网站导航

- [首页](/)
- [所有笔记](/notes/)
- [笔记分类](/categories/)
- [关于](/about/)
- [网站导航](/doc/nav.md)
- [Markdown 语法参考](/doc/markdown.md)