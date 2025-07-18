from django import forms
from comment.models import Comment, Contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "subject", "message"]


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = "__all__"
