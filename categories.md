---
layout: default
title: 笔记分类
permalink: /categories/
---

<div class="categories">
  <h1 class="page-heading">笔记分类</h1>

  {% comment %}
  按类别分组文章
  {% endcomment %}
  {% assign categories = site.posts | map: 'tags' | join: ',' | split: ',' | uniq | sort %}
  
  {% for category in categories %}
    {% assign posts_in_category = site.posts | where_exp: "post", "post.tags contains category" %}
    {% if posts_in_category.size > 0 %}
      <div class="category-section">
        <h2 id="{{ category | slugify }}">{{ category | capitalize }}</h2>
        <ul>
          {% for post in posts_in_category %}
            <li>
              <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              <span class="post-date">- {{ post.date | date: "%Y-%m-%d" }}</span>
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endif %}
  {% endfor %}
</div>