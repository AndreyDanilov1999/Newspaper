from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import ModelForm
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
    add_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    add_date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата создания',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    add_category = ModelChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Категория поста',
        empty_label='all'
    )


class FormNews(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'postCategory']


class FormArticle(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'postCategory']



