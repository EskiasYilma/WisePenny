from django import template
# from ..models import Countries

register = template.Library()


@register.simple_tag
def get_addressee():
    return "World"


@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    try:
        return d[k]
    except Exception as e:
        return 0


# @register.filter(name='lower_case')
# def lower_case(d):
#     '''Returns the given key from a dictionary.'''
#     try:
#         ctr_name = Countries.objects.get(country_name=d).country_iso
#         return ctr_name.lower()
#     except Exception as e:
#         return 0
