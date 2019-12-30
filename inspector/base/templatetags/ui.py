from django.template import Library
from django.utils.safestring import mark_safe

from inspector.base.constants import ICONS, STATUS_ICONS, RESULT_ICONS

register = Library()


@register.simple_tag(name="fa")
def fa(entity):
    return mark_safe(ICONS[entity])


@register.simple_tag(name="fa_status")
def fa_status(entity):
    return mark_safe(STATUS_ICONS[entity.status])


@register.simple_tag(name="fa_result")
def fa_result(entity):
    return mark_safe(RESULT_ICONS[entity.result])
