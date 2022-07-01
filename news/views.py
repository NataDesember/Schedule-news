# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

from .filters import PostFilter
from .models import Post, PostCategory, Category, UserCategory
from .forms import PostForm, BaseRegisterForm, PostUpdateForm


# Список статей
class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'page'
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    # Фильтры со страницами вместе не работали, или одно или другое
    # Где ошиблась с описанием - не нашла.
    #
    # Решила сделать как тут (нашла в гугле)
    # https://stackoverflow.com/questions/44048156/django-filter-use-paginations
    #
    # В итоге фильтры и paginator вызваны руками в нужном порядке
    # и подставлены в результат - страница с данными, объект страницы, и фильтр для формы
    #
    # Также использовала query_transform для формирования правильных URL для перехода
    # между страницами paginator по результатам фильтра (подсмотрела там же)
    def get(self, request, *args, **kwargs):
        sfilter = PostFilter(request.GET, queryset=self.get_queryset())
        filtered_qs = sfilter.qs
        paginator = Paginator(filtered_qs, self.paginate_by)
        page = request.GET.get('page', 1)

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        return render(request, 'news.html', {
            'page': result,
            'page_obj': result,
            'filter': sfilter,
            'is_author': self.request.user.groups.filter(name='authors').exists()
        })


# Одна статья в деталях
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        post = self.get_object(self.queryset)

        subscribed = ''
        for category in post.categorys.all():
            for sub in category.subscribers.all():
                if sub.email == request.user.email:
                    subscribed = subscribed + category.category_name + ','

        return render(request, self.template_name, {
            'post': post,
            'subscribed': subscribed,
        })


# Создание новой статьи
class PostCreateView(CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post')
    request_user = None

    def post(self, request, *args, **kwargs):
        self.request_user = request.user
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request_user = self.request_user
        return form


# Альтернативный показ одной статьи, из прошлого урока
class PostDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'


# Редактирование статьи
class PostUpdateView(UpdateView):
    template_name = 'news/post_update.html'
    form_class = PostUpdateForm
    model = Post

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
    # редактировать
    def get_object(self, **kwargs):
        sid = self.kwargs.get('pk')
        return Post.objects.get(pk=sid)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.request_user = request.user
        return super().post(request, *args, **kwargs)


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'news/create.html'


# Удаление статьи с запросом подтверждения
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post', 'news.change_post')


# ручной поиск по заголовку в отдельной странице, проба пера
class SearchNews(ListView):
    def get(self, request):
        news = Post.objects.filter(title__contains=request.GET.get('q')).order_by('-time_in')
        data = {
            'found': news,
        }
        return render(request, 'search.html', data)


class IndexView(LoginRequiredMixin, PostList):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


class AddPost(PermissionRequiredMixin, PostCreateView):
    permission_required = ('news.add_post', )


class ChangePost(PermissionRequiredMixin, PostUpdateView):
    permission_required = ('news.change_post', )


class DeletePost(PermissionRequiredMixin, PostDeleteView):
    permission_required = ('news.delete_post', )


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


# http://127.0.0.1:8000/news/subscribe/3
@login_required
def subscribe_me(request, category_id):
    user = request.user
    category = Category.objects.filter(id=category_id)[0]

    user_category_exists = UserCategory.objects.filter(user=user, category=category).exists()
    if not user_category_exists:
        uc = UserCategory.objects.create(user=user, category=category)

    return redirect('/news/')


# http://127.0.0.1:8000/news/unsubscribe/3
@login_required
def unsubscribe_me(request, category_id):
    user = request.user
    category = Category.objects.filter(id=category_id)[0]

    user_category_exists = UserCategory.objects.filter(user=user, category=category).exists()
    if user_category_exists:
        UserCategory.objects.filter(user=user, category=category).delete()

    return redirect('/news/')

