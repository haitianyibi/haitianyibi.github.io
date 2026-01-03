---
layout: default
title: 所有笔记
permalink: /notes/
---

<div class="posts">
  <h1 class="page-heading">所有笔记</h1>

  <ul class="post-list">
    {% for post in site.posts %}
      <li>
        <h2>
          <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
        </h2>
        <span class="post-meta">{{ post.date | date: "%Y-%m-%d" }}</span>
        {% if post.tags.size > 0 %}
          <span class="post-tags">
            {% for tag in post.tags %}
              <span class="tag">{{ tag }}</span>
            {% endfor %}
          </span>
        {% endif %}
        <div class="post-excerpt">
          {% if post.excerpt %}
            {{ post.excerpt | strip_html | truncate: 160 }}
          {% else %}
            {{ post.content | strip_html | truncate: 160 }}
          {% endif %}
        </div>
      </li>
    {% endfor %}
  </ul>
</div>