from django import template

register = template.Library()


# Добавление номера страницы без повторов и с сохранением фильтра. Взято тут
# https://stackoverflow.com/questions/44048156/django-filter-use-paginations
@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()
