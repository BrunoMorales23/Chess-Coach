from django import forms
from django.contrib.auth.models import User

#class RegisterForm(forms.Form):
#    username = forms.CharField(label='Usuario', max_length=100)
#    email = forms.EmailField(label='Correo electrónico')
#    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # encripta la password
        if commit:
            user.save()
        return user