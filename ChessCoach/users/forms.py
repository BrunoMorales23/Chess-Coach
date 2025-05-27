from django import forms
from django.contrib.auth.models import User

#class RegisterForm(forms.Form):
#    username = forms.CharField(label='Usuario', max_length=100)
#    email = forms.EmailField(label='Correo electrónico')
#    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    confirmpassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean(self):
        global validation
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmpassword = cleaned_data.get("confirmpassword")
        print(password)
        print(confirmpassword)
        
        if password != confirmpassword:
            raise forms.ValidationError("Las contraseñas no coinciden")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user