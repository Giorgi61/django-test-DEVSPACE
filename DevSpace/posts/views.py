from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import FilterForm
from .models import Post

# Create your views here.


class PostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'
    extra_context = {'title': 'Posts'}
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = FilterForm(self.request.GET)

        page_obj = context.get('page_obj')
        paginator = context.get('paginator')
        paginated_range = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=2)
        context['paginated_range'] = paginated_range

        return context

    def get_queryset(self):
        if self.request.GET.get('my_posts'):
            return self.model.objects.filter(author=self.request.user.pk)

        return self.model.objects.all()


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/detail_post.html'
    extra_context = {'title': 'Post'}

    def get_queryset(self):
        return Post.objects.filter(uuid=self.kwargs['uuid'])


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/create_edit_post.html'
    fields = ['title', 'text', 'image']
    extra_context = {'title': 'Edit Post'}



    def get_queryset(self):
        return self.model.objects.filter(uuid=self.kwargs['uuid'], author=self.request.user.pk)

    # def get_success_url(self):
    #     return reverse('posts:detail_post', kwargs={'uuid': self.kwargs['uuid'], 'slug': self.kwargs['slug']})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/create_edit_post.html'
    fields = 'title', 'text', 'slug', 'image'
    extra_context = {'title': 'Create Post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

