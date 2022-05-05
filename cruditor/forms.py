from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from tapeforms.contrib.bootstrap import BootstrapTapeformMixin


class CruditorTapeformMixin(BootstrapTapeformMixin):
    """
    Cruditor mixin for all forms (relies on django-tapeforms).
    """
    pass


class CruditorFormsetMixin(object):
    """
    Helper mixin to provide some additional configuration to the javascript part
    of Cruditor's formset support, mainly translations but also all other stuff
    which might be needed.
    """
    js_formset_options = None
    new_item_label = _('New item')

    def add_fields(self, form, index):
        """
        Overwritten method to make sure the DELETE marker field is hidden in output.
        """
        super().add_fields(form, index)

        if DELETION_FIELD_NAME in form.fields:
            form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()

    def get_js_formset_options(self):
        """
        This method builds the options dict for the javascript part. Some defaults
        are merged with `js_formset_options` property.
        """
        options = {
            'prefix': self.prefix,
            'add-button-label': gettext('Add another'),
            'add-title': self.new_item_label,
            'delete-button-label': gettext('Delete item'),
            'delete-confirm-text': gettext(
                'Are you sure? Item will be deleted after saving.')
        }
        options.update(self.js_formset_options or {})
        return options


class CruditorFormsetFormMixin(CruditorTapeformMixin):
    """
    Helper mixin for forms in a formset, used together with Cruditor-enabled
    formsets.
    """

    @cached_property
    def template_context(self):
        return self.get_template_context()

    def get_template_context(self):
        return {}

    def visible_fields(self):
        """
        This method is overwritten to  make sure that the DELETE marker field
        is not considered when returning the list of visible fields.
        """
        return [
            field for field in super().visible_fields()
            if field.name != DELETION_FIELD_NAME
        ]

    def hidden_fields(self):
        """
        This method is overwritten to  make sure that the DELETE marker field
        is not considered when returning the list of hidden fields.
        Cruditor template renders the field manually.
        """
        return [
            field for field in super().hidden_fields()
            if field.name != DELETION_FIELD_NAME
        ]


class LoginForm(CruditorTapeformMixin, AuthenticationForm):
    """
    Tapeform-enabled version of the Django AuthenticationForm.
    """
    pass


class ChangePasswordForm(CruditorTapeformMixin, SetPasswordForm):
    """
    Tapeform-enabled version of the Django SetPasswordForm.
    """
    pass
