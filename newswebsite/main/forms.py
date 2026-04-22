from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewsForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError('Заголовок должен быть не короче 10 символов!')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 500:
            raise forms.ValidationError('Текст новости не может быть длиннее 500 символов!')
        return content

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg', '.gif']:
                raise forms.ValidationError('Можно загружать только изображения (PNG, JPG, JPEG, GIF)!')
        return image

    class Meta:
        model = News
        fields = ['title', 'content', 'image']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 10:
            raise ValidationError('Имя пользователя должно содержать минимум 10 символов!')
        pattern = r'^[a-zA-Zа-яА-Я0-9]+$'
        if not re.match(pattern, username):
            raise ValidationError('Имя пользователя может содержать только буквы (русские/английские) и цифры!')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну латинскую букву!')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру!')
        special_chars = r'[!@#$%^&*()_\-+=]'
        if not re.search(special_chars, password):
            raise ValidationError('Пароль должен содержать хотя бы один специальный символ (!@#$%^&*()_-+=)!')
        return password