from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'you@mail.com'}),
    )
    phone = forms.CharField(
        max_length=30,
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': '+996 (___) ___-__-__'}),
    )
    message = forms.CharField(
        max_length=5000,
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о проекте'}),
    )
