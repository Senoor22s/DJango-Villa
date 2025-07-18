{% extends 'mail_templated/base.tpl' %}
{% block subject %}
Reset password
{% endblock %}
{% block html %}
http://127.0.0.1:8080/accounts/api/v1/reset-password/confirm/{{token}}
{% endblock %}