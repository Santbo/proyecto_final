from typing import Any, Dict
from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ComentarioForm
from .models import Comentario
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/individual_post.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'id'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        return context
    
    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario =form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            print(self.kwargs['id'])
            comentario.save()
            return redirect('apps.posts:individual_post', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
        


class DeletePostView(DeleteView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/delete_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        messages.success(self.request, 'Noticia borrada!')
        return super().form_valid(form)


class AddPostView(CreateView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/add_post.html'
    fields = ('titulo', 'texto', 'categoria', 'imagen')
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        messages.success(self.request, 'Noticia creada!')
        return super().form_valid(form)


class EditPostView(UpdateView):
    model = Post
    template_name = 'posts/edit_post.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'id'
    fields = ('titulo', 'texto', 'categoria', 'imagen')
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        messages.success(self.request, 'Noticia actualizada!')
        return super().form_valid(form)

   
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.post_id = self.kwargs['posts_id']
        return super().form_valid(form)



    
