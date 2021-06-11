from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

"""
posts = [
    {
        'author': 'Jack Sebastian',
        'title' : 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 23, 2021'
    },
    {
        'author': 'Liann Sebastian',
        'title' : 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 25, 2021'
    }
]
"""

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<modal>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<modal>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object() # obtain info from post
        if self.request.user == post.author: # only the author of post can make updates
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object() # obtain info from post
        if self.request.user == post.author: # only the author of post can make updates
            return True
        return False

     
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

