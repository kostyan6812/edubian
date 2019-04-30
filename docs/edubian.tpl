{%- extends 'full.tpl' -%}


{%- block header -%}
<!DOCTYPE html>
<html>
<head>
{%- block html_head -%}
<meta charset="utf-8" />
{% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
<h1>{{nb_title}}</h1>
{% endblock html_head %}
</head>
</html>
{% endblock header %}
