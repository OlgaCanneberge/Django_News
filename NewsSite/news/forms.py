from django import forms
from .models import Article
from ckeditor.widgets import CKEditorWidget


class ArticleCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """

    text = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor'))

    class Meta:
        model = Article
        fields = ('title', 'category', 'description', 'text', 'thumbnail')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            
            
class ArticleUpdateForm(ArticleCreateForm):
    """
    Форма обновления статьи на сайте
    """

    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        # self.fields['fixed'].widget.attrs.update({
        #     'class': 'form-check-input'
        # })


from .models import Comment

class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)

    # def form_valid(self, form):
    #     form.instance.article = Article.objects.get(pk=self.kwargs.get("pk"))
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)