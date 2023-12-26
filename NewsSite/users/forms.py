from django import forms

from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """
    username = forms.CharField(max_length=100, label='Логин',
                               widget=forms.TextInput(
                                   attrs={"class": "form-control mb-1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    first_name = forms.CharField(max_length=100, label='Ваше имя',
                                 widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(max_length=100, label='Ваша фамилия', required=False,
                                widget=forms.TextInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
#
#     def clean_email(self):
#         """
#         Проверка email на уникальность
#         """
#         email = self.cleaned_data.get('email')
#         username = self.cleaned_data.get('username')
#         if email and User.objects.filter(email=email).exclude(username=username).exists():
#             raise forms.ValidationError('Email адрес должен быть уникальным')
#         return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """

    birth_date = forms.DateField(label='Дата рождения', required=False,
        widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    bio = forms.CharField(max_length=500, label='О себе', required=False,
                          widget=forms.Textarea(attrs={'rows': 5, "class": "form-control mb-1"}))

    avatar = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')



class UserRegisterForm(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'введите логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'введите свой email'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'имя'})
            self.fields["last_name"].widget.attrs.update({"placeholder": 'фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'придумайте свой пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'повторите придуманный пароль'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['username'].label = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })



class UserPasswordChangeForm(SetPasswordForm):
    """
    Форма изменения пароля
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })







