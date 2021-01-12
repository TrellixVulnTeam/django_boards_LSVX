from django import forms
from .models import Topic, Comment


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'type your fuken message', 'rows': 7}
    ), max_length=10000)

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
