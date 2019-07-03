from django.template import Library

register = Library()


@register.filter
def highlight(income_object, s_pattern):
    return income_object.replace(s_pattern, f'<span class="hl">{s_pattern}</span>')
