from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class CustomUserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = '__all__'
        
    username = forms.CharField(required=True, max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupUsername',
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupPassword',
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if not captcha:
            self.add_error('captcha', ValidationError('Вы не прошли капчу', code='invalid'))
            return cleaned_data
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            for field in ['username', 'password']:
                self.add_error(field, ValidationError('Неправильное имя пользователя или пароль', code='invalid'))

        return cleaned_data
  