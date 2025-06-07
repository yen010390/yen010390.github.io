---
layout: default
title: "Category 1: Global Quality Systems & Process Harmonization"
excerpt: "This category showcases leadership in driving quality improvements across global standards and harmonizing international processes to enhance efficiency and compliance."
collection: category
permalink: /category/global-quality-systems/
category: "Category 1: Global Quality Systems & Process Harmonization"
---

<h2>Projects in category: {{ page.category }}</h2>

<style>
  .project-item {
    border-left: 5px solid #2a7ae2;
    border: 1px solid #ddd;
    background: #fefefe;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 6px;
  }
  .project-title {
    font-weight: 700;
    font-size: 1.3em;
    margin-bottom: 8px;
  }
  .project-tags {
    margin-top: 10px;
    font-size: 0.9em;
    color: #555;
  }
  .project-tags span {
    background-color: #e3e3e3;
    border-radius: 3px;
    padding: 2px 8px;
    margin-right: 6px;
    display: inline-block;
  }
</style>

{% assign all_projects = site.project.docs %}
{% assign projects_in_category = all_projects | where:"category", page.category %}

{% if projects_in_category.size > 0 %}
  {% for project in projects_in_category %}
    <div class="project-item">
      <div class="project-title">
        <a href="{{ project.url | relative_url }}">{{ project.title }}</a>
      </div>
      <div class="project-excerpt">
        {{ project.excerpt | strip_html | truncatewords: 40 }}
      </div>
      {% if project.tags %}
        <div class="project-tags">
          {% for tag in project.tags %}
            <span>#{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
{% else %}
  <p>No projects found in this category.</p>
{% endif %}
