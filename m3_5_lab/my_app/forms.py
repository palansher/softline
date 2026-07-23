from django import forms

from my_app.models import Article


class UserForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=20,required=True)
    comment = forms.CharField(widget=forms.Textarea,label='Комментарий')
    age = forms.IntegerField(label='Возраст')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        db_table = 'article'

