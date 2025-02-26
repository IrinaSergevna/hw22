from django import template

register = template.Library()

@register.filter
def truncate_with_ellipsis(value, max_length):
    """
    Обрезает текст до max_length символов и добавляет '...', если текст длиннее.
    """
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value