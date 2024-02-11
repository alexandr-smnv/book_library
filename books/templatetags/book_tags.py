from django.template.defaulttags import register


@register.filter
def get_value(dictionary, key):
    """
    Получение значения по ключу в словаре
    :param dictionary: словарь
    :param key: ключ
    :return: Значение по ключу
    """
    return dictionary.get(key)


@register.filter
def multiplication(a, b):
    """
    Умножение значений
    """
    return int(a) * int(b)
