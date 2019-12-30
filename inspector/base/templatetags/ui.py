from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from inspector.base.constants import ICONS, STATUS_ICONS, RESULT_ICONS

register = Library()


@register.simple_tag
def fa(entity):
    return mark_safe(ICONS[entity])


@register.simple_tag
def fa_status(entity):
    return mark_safe(STATUS_ICONS[entity.status])


@register.simple_tag
def fa_result(entity):
    return mark_safe(RESULT_ICONS[entity.result])


@register.simple_tag
def fa_l(entity):
    return mark_safe(f'<p class="text-left">{ICONS[entity]}</p>')


@register.simple_tag
def fa_c(entity):
    return mark_safe(f'<p class="text-center">{ICONS[entity]}</p>')


@register.filter
@stringfilter
def p_c(value):
    return mark_safe(f'<p class="text-center">{value}</p>')


@register.filter
@stringfilter
def p_l(value):
    return mark_safe(f'<p class="text-left">{value}</p>')
