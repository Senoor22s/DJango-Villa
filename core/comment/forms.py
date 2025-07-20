from django import forms
from comment.models import Comment, Contact
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "subject", "message"]


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Contact
        fields = "__all__"
