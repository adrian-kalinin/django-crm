from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class AgentModelForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name'
        )
