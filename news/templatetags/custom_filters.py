from django import template

register = template.Library()

bad_words = ['редиска', 'Байден', 'Маск', 'Musk']


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    """
   value: значение, к которому нужно применить фильтр
   """
    # Возвращаемое функцией значение подставится в шаблон.

    v = f'{value}'
    for s in bad_words:
        v = v.replace(s, s[0] + make_chars(len(s) - 1))
    return v


def make_chars(count):
   s = ''
   for i in range(count):
      s = s + '*'
   return s

