---
layout: default
title: 我的笔记库
---

<div class="home">

  <div class="hero">
    <h1 class="page-heading">{{ page.title }}</h1>
    <p class="lead">{{ site.description }}</p>

    <div class="hero-actions">
      <a class="btn" href="{{ '/' | relative_url }}">首页</a>
      <a class="btn secondary" href="{{ '/notes/' | relative_url }}">查看所有笔记</a>
    </div>
  </div>

  <h2 class="post-list-heading">最新笔记</h2>
  <ul class="post-list">
    {% for post in site.posts limit: 10 %}
      <li>
        <article class="post-card">
          <div class="post-meta">{{ post.date | date: "%Y-%m-%d" }}</div>
          <h3 class="post-title">
            <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
          </h3>

          {% if post.excerpt %}
            <div class="post-excerpt">
              {{ post.excerpt | strip_html | truncate: 200 }}
            </div>
          {% endif %}

          {% if post.tags %}
            <div class="post-tags">
              <ul class="tag-list">
                {% for tag in post.tags %}
                  <li class="tag">{{ tag }}</li>
                {% endfor %}
              </ul>
            </div>
          {% endif %}
        </article>
      </li>
    {% endfor %}
  </ul>

  {% if paginator %}
    {% if site.posts.size > 0 %}
      <div class="pager">
        <ul class="pagination">
        {% if paginator.previous_page %}
          <li><a href="{{ paginator.previous_page_path | relative_url }}">Previous</a></li>
        {% endif %}

        <li><strong class="page active">{{ paginator.page }}</strong></li>

        {% if paginator.next_page %}
          <li><a href="{{ paginator.next_page_path | relative_url }}">Next</a></li>
        {% endif %}
        </ul>
      </div>
    {% endif %}
  {% endif %}

  <p class="rss-subscribe">订阅 <a href="{{ "/feed.xml" | relative_url }}">RSS</a> 获取最新笔记</p>

</div>
