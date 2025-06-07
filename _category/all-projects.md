---
layout: default
title: "All Projects by Category"
permalink: /projects/
---

{% include base_path %}
{% include group-by-array collection=site.project field="category" %}

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

{% assign ordered_categories = 
  "Category 1: Global Quality Systems & Process Harmonization,
   Category 2: Digitalization & SAP-Integrated Process Control,
   Category 3: Lean Manufacturing & Continuous Improvement,
   Category 4: Advanced Process Analysis & Simulation,
   Category 5: Others" | split: "," %}

{% for ordered_cat in ordered_categories %}
  {% assign category = ordered_cat | strip %}
  {% assign index = group_names | index_of: category %}
  {% if index != -1 %}
    {% assign projects = group_items[index] %}
    <h2 id="{{ category | slugify }}" class="archive__subtitle">{{ category }}</h2>
    
    {% for project in projects %}
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
  {% endif %}
{% endfor %}
