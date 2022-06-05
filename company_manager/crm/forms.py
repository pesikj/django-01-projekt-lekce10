from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError, CharField
from django.utils.translation import gettext as _
from ckeditor.widgets import CKEditorWidget

from crm.models import Employee, Company, Opportunity


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('department', 'phone_number')


class OpportunityForm(ModelForm):
    class Meta:
        model = Opportunity
        fields = ["company", "primary_contact", "description", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("company", css_class="col-sm-4"),
                Div("primary_contact", css_class="col-sm-4"),
                Div("status", css_class="col-sm-4"),
                Div("description", css_class="col-sm-12"),
                css_class="row",
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button')
            )
        )

class CompanyForm(ModelForm):
    notes = CharField(widget=CKEditorWidget())

    def clean_identification_number(self):
        identification_number = self.cleaned_data['identification_number']

        if len(identification_number) != 8:
            raise ValidationError(_("The identification number has incorrect length."))
        if not identification_number.isdigit():
            raise ValidationError(_("The identification number must contain only numbers."))
        return identification_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if "@" not in email:
                raise ValidationError(_("Email does not contain @."))
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number:
            if phone_number.startswith("+420"):
                if len(phone_number) != 13:
                    raise ValidationError(_("Incorrect format of phone number"))
            else:
                if len(phone_number) != 9:
                    raise ValidationError(_("Incorrect format of phone number"))
        return phone_number

    class Meta:
        model = Company
        fields = ["name", "status", "phone_number", "email", "identification_number", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("name", css_class="col-sm-4"),
                Div("status", css_class="col-sm-2"),
                Div("identification_number", css_class="col-sm-4"),
                Div("email", css_class="col-sm-4"),
                Div("phone_number", css_class="col-sm-4"),
                Div("notes", css_class="col-sm-12"),
                css_class="row",
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button')
            )
        )


class RegisterUserForm(UserCreationForm):
    username = CharField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
