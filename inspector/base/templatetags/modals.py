from django.template import Library

register = Library()


@register.inclusion_tag("components/modals_modal.html")
def modals_modal(modal_id):
    return {"id": modal_id}


@register.inclusion_tag("components/modals_js.html")
def modals_js(action, object_type):
    return {"object": object_type, "action": action}
