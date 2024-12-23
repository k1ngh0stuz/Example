from django import forms
from .models import Article  # Под какую модель будем создавать формы
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):  # Что форма зависит от полей модельки
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'photo',
            'is_publisher',
            'category'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название',
                'class': 'form-control'
            }),
            'content': forms.Textarea({
                'placeholder': 'Описание',
                'class': 'form-control'
            }),
            'is_publisher': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })

        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователья',
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control'
                                   }
                               ))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control'
                               })
                               )


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователья", max_length=155, help_text='Максимум 155 символов',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователья'
                               }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите электронную почту'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
