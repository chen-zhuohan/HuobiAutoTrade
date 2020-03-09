from flask_admin.form import fields
import json
from jinja2 import Markup


def json_formatter(view, context, model, name):
    """
    for example:
        column_formatters = {
            'kwargs': json_formatter,
        }
    """
    value = getattr(model, name)
    json_value = json.dumps(value, ensure_ascii=False, indent=0)
    return Markup('<pre>{}</pre>'.format(json_value))


class JSONField(fields.JSONField):
    """
    for example:
        form_overrides = {
            'kwargs': JSONField,
    }
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return json.dumps(self.data, ensure_ascii=False, indent=2)
        else:
            return ''