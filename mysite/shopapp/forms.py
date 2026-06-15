from django import forms
from shopapp.models import User

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    
    id = forms.CharField(label="会員ID")
    password = forms.CharField(label = "パスワード")
    
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get("id")
        password = cleaned_data.get("password")
        if not User.objects.filter(user_id=id, password=password).exists():
            raise forms.ValidationError("会員IDかパスワードが正しくありません")
        return cleaned_data

class UserRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    
    user_id = forms.CharField(label="会員ID")
    password1 = forms.CharField(label = "パスワード")
    password2 = forms.CharField(label = "パスワード確認")
    name = forms.CharField(label = "お名前")
    address = forms.CharField(label = "ご住所")
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        errors = []
        if password1 != password2:
            errors.append("パスワードと確認用パスワードが一致しません")
        if User.objects.filter(user_id=user_id).exists():
            errors.append("この会員IDはすでに使用されています")
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
    
class UserUpdateForm(forms.Form):
    def __init__(self, *args,original_user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.original_user_id = original_user_id
    
    user_id = forms.CharField(label="会員ID")
    password1 = forms.CharField(label = "パスワード")
    password2 = forms.CharField(label = "パスワード確認")
    name = forms.CharField(label = "お名前")
    address = forms.CharField(label = "ご住所")
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        errors = []
        if password1 != password2:
            errors.append("パスワードと確認用パスワードが一致しません")
        if user_id != self.original_user_id:
            if User.objects.filter(user_id=user_id).exists():
                errors.append("この会員IDはすでに使用されています")
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
    
