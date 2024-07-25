from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        labels = {'name': '', 'lang': '', 'code': ''}
        widgets = {
          'name': TextInput(
              attrs={"class":"form-control", 'style': 'max-width: 350px;', 'placeholder': 'Название сниппета'}
              ),
          'code': Textarea(
              attrs={"class":"form-control", 'style': 'max-width: 350px;', 'placeholder': 'Код сниппета'}
              ),
        }


