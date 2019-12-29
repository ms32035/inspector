from crispy_forms.layout import HTML


def fa_icon(icon: str, title: str, style: str = "fas"):
    return f'<i class="{style} fa-{icon}" title="{title}"></i>'


def button_reset(url: str):
    return HTML(
        '<a class="btn btn-outline-danger btn-block btn-sm" href={% url "'
        + url
        + '" %}>Reset</a>'
    )
