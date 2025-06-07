{% include base_path %}
{% include group-by-array collection=site.project field="category" %}

{% for category in group_names %}
  {% assign projects = group_items[forloop.index0] %}
  <h2 id="{{ category | slugify }}" class="archive__subtitle">{{ category }}</h2>

  {% for project in projects %}
    <div class="project-item">
      <div class="project-title">
        <a href="{{ project.url | relative_url }}">{{ project.title }}</a>
      </div>
      <div class="project-excerpt">
        {{ project.excerpt | strip_html | truncatewords: 40 }}
      </div>
      {% if project.tag %}
        <div class="project-tags">
          {% for tag in project.tag %}
            <span>#{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
{% endfor %}


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
