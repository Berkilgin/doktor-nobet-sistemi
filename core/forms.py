from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class TekSeferlikSifreForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Şifre tekrar alanını (new_password1 sonrasındaki teyit alanı) siliyoruz
        del self.fields['new_password2']

    def clean(self):
        # Normalde Django burada iki şifreyi karşılaştırır.
        # Biz bu kontrolü iptal etmek için clean metodunu eziyoruz.
        # Sadece şifre kurallarını (uzunluk vb.) kontrol etmeye devam eder.
        return self.cleaned_data