from typing import List
from django.shortcuts import redirect
#from lib2to3.pgen2.pgen import DFAState
from django.shortcuts import render
from .models import Post#, User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import ChangePassForm, PostForm, SignUpForm, LogInForm
from django.views.generic.list import ListView #new line
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib import messages


# Create your views here.
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts':posts})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form':form})

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})

#Lists the public posts on the homepage
class PostView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(published_date__lte=timezone.now(), private=False).order_by('-published_date')

#Lists the private, draft posts
class PostDraft(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs).filter(published_date__lte=timezone.now(), private=True)
        if self.request.user.is_superuser:
            return query.order_by("-published_date")
        return query.filter(author=self.request.user).order_by("-published_date")
    

#Shows a detailed view of a post
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    
    #user authorization check
    def get_queryset(self, *args, **kwargs):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_superuser or self.request.user == obj.author:
            return super().get_queryset()
        return super().get_queryset(*args, **kwargs).filter(published_date__gt=timezone.now())
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.add_message(request, messages.INFO, "You don't have permission to edit that post!")
            return redirect('post_list')
        return super().get(request, *args, **kwargs)
    
    
#View to create new posts
class PostNew(LoginRequiredMixin, CreateView):
    model = Post
    form = PostForm
    template_name_suffix = '_edit'
    fields= PostForm.Meta.fields
    
    #saves necessary information
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date=timezone.now()
        if 'Publish' in self.request.POST:
            post.private = False
        elif 'Draft' in self.request.POST:
            post.private = True
        post.save()
        return redirect('post_detail', pk=post.pk)

#View to edit existing post
class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form = PostForm
    template_name_suffix = '_edit'
    
    fields= ['title', 'text']
    
    #authorization check
    def get_queryset(self, *args, **kwargs):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_superuser:
            return super().get_queryset()
        if self.request.user == obj.author:
            return super().get_queryset()
        return super().get_queryset(*args, **kwargs).filter(published_date__gt=timezone.now())
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.add_message(request, messages.INFO, "You don't have permission to edit that post!")
            return redirect('post_list')
        return super().get(request, *args, **kwargs)

    #updates information
    def form_valid(self, form):
        post = form.save(commit=False)
        # if post.author is not self.request.user:
        #     return redirect('post_detail', pk=post.pk)
        post.author = self.request.user
        post.published_date=timezone.now()
        if 'Publish' in self.request.POST:
            post.private = False
        elif 'Draft' in self.request.POST:
            post.private = True
        post.save()
        return redirect('post_detail', pk=post.pk)
    
#View for the search function
class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name_suffix = '_search'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs).filter(title__icontains=self.request.GET.get("mySearch")).order_by('-published_date')
        return super().get_queryset(*args, **kwargs).filter(title__icontains=self.request.GET.get("mySearch")).exclude(~Q(author=self.request.user), private=True).order_by('-published_date')
        
#View to delete posts
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '_delete'
    
    success_url = reverse_lazy("post_list")
    
    #authorization check
    def get_queryset(self, *args, **kwargs):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_superuser:
            return super().get_queryset()
        if self.request.user == obj.author:
            return super().get_queryset()
        return super().get_queryset(*args, **kwargs).filter(published_date__gt=timezone.now())
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.add_message(request, messages.INFO, "You don't have permission to delete that post!")
            return redirect('post_list')
        return super().get(request, *args, **kwargs)

#login view
class LogIn(CreateView):
    model = User
    form_class = LogInForm
    template_name = 'login.html'
    
#signup view
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy("post_list")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("post_list")

#View to change password
class ChangePassword(UpdateView):
    model = User
    form_class = ChangePassForm
    template_name = 'changepass.html'
    success_url = reverse_lazy("settings")
    fields = ['password']
    success_url = reverse_lazy("post_list")
    
    def form_valid(self, form):
        form.save()
        return redirect('accounts/login')


# def login_view(request):
#     #username = request.POST['username']
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         success_url = reverse("post_list")
#     else:
#         return redirect('post_list')
    

# def signup(request):
# 	if request.method == "POST":
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("post_list")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = SignUpForm()
# 	return render (request=request, template_name="signup.html")



def change_password(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        u=User.objects.get(username=username)
        u.set_password(new_password)
        u.save()
        logout(request)
        return redirect('accounts/login/')
    else:
        return redirect('post_list')