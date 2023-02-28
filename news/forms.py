from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):

   heading = forms.CharField(label='Заголовок поста')
   #category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
   text = forms.CharField(min_length=20, label='Текст поста')


   class Meta:
       model = Post
       fields = [
           'heading',
           'text',
           'category',
           'author',
       ]

   '''def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("text")
       if text is not None and len(text) < 20:
           raise ValidationError({
               "text": "Текст поста не может быть менее 20 символов."
           })

       return cleaned_data'''