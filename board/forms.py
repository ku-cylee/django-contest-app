from django import forms

USERNAME_MAX = 15
PASSWORD_MAX = 20
EMAIL_MAX = 50

CATEGORY_NAME_MAX = 10
ARTICLE_TITLE_MAX = 40
COMMENT_MAX = 300


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=USERNAME_MAX, widget=forms.TextInput({
        'class': 'form-control',
        'aria-label': 'Username',
        'aria-describedby': 'username-addon',
    }))
    password = forms.CharField(max_length=PASSWORD_MAX, widget=forms.PasswordInput({
        'class': 'form-control',
        'aria-label': 'Password',
        'aria-describedby': 'password-addon',
    }))
    email = forms.CharField(max_length=EMAIL_MAX, widget=forms.TextInput({
        'class': 'form-control',
        'aria-label': 'Email',
        'aria-describedby': 'email-addon',
    }))


class SignInForm(forms.Form):
    username = forms.CharField(max_length=USERNAME_MAX, widget=forms.TextInput({
        'class': 'form-control',
        'aria-label': 'Username',
        'aria-describedby': 'username-addon'
    }))
    password = forms.CharField(max_length=PASSWORD_MAX, widget=forms.PasswordInput({
        'class': 'form-control',
        'aria-label': 'Password',
        'aria-describedby': 'password-addon'
    }))


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=CATEGORY_NAME_MAX, widget=forms.TextInput({
        'class': 'form-control',
        'aria-label': 'Name',
        'aria-describedby': 'name-addon',
    }))


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=ARTICLE_TITLE_MAX, widget=forms.TextInput({
        'class': 'form-control mb-2',
    }))
    content = forms.CharField(widget=forms.Textarea({
        'id': 'editor',
    }))


class CommentForm(forms.Form):
    content = forms.CharField(max_length=COMMENT_MAX, widget=forms.Textarea({
        'class': 'form-control mb-2',
        'rows': 5,
    }))
