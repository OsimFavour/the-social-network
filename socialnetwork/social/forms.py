from django import forms
from .models import Post, Comment, MessageModel


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
        })
    )
    # Required=False -> so that it doesn't give an error when trying to submit
    # a post without an imgae
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "allow_multiple_selected": True
        })
        # widget=forms.ClearableFileInput()
    )

    # widget=forms.ClearableFileInput(), required=False

    class Meta:
        """The meta class sets the models and the fields to save
           to the database
        """
        model = Post
        fields = ['body']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Comment Here...'
        })
    )

    class Meta:
        model = Comment
        fields = ['comment']


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.ModelForm):
    # You have to have the meta class in the parent class
    # of the model form
    body = forms.CharField(label='', max_length=1000)
    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']


class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Share Something...'
        })
    )

class ExploreForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Explore tags'
        })
    )