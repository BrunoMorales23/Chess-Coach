from django import forms
from django.contrib.auth.models import User
from .models import CustomUser

#class RegisterForm(forms.Form):
#    username = forms.CharField(label='Usuario', max_length=100)
#    email = forms.EmailField(label='Correo electrónico')
#    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    confirmpassword = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use, please, try another.")
        return username
 
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use, please, try another.")
        return email
 
    def clean(self):
        global validation
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmpassword = cleaned_data.get("confirmpassword")
        if password != confirmpassword:
            raise forms.ValidationError("Password doesn't match, try again.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    