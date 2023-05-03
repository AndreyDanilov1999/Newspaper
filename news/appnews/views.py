from django.core.cache import cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category, Subscriber
from .filters import PostFilter, FormNews, FormArticle
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('id')
    return render(
        request,
        'sections/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class NewsList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'sections/list_news.html'
    context_object_name = 'list_news'
    paginate_by = 10


class SearchNews(ListView):
    model = Post
    template_name = 'sections/search_page.html'
    context_object_name = 'search_page'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class SingleNews(DetailView):
    model = Post
    template_name = 'single_news.html'
    context_object_name = 'single'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class CreateNews(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'appnews.add_post'
    form_class = FormNews
    model = Post
    template_name = 'sections/create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "NW"
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class CreateArticle(PermissionRequiredMixin, CreateView):
    permission_required = 'appnews.add_post'
    form_class = FormArticle
    model = Post
    template_name = 'sections/create_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "AR"
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class EditNews(PermissionRequiredMixin, UpdateView):
    permission_required = 'appnews.change_post'
    form_class = FormNews
    model = Post
    field = ['title', 'text', 'postCategory']
    template_name = 'edit.html'
    context_object_name = 'edit'
    success_url = reverse_lazy('main')


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = 'appnews.delete_post'
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('main')
