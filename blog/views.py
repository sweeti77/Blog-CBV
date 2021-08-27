from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import (
        ListView, DetailView, CreateView, UpdateView, DeleteView)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Blog, Category
from .forms import BlogForm, CategoryForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth import get_user_model

from django.core.paginator import Paginator

user = get_user_model()



# DetailView/ DeleteView (similar)
# CreateView/ UpdateView (similar)

class List_View(ListView):
    model = Blog
    queryset = Blog.objects.filter(status="Publish").order_by('-posted_date')
    # ordering = ['-posted_date'] #same as above

    template_name = 'blog/ListView.html'
    context_object_name = 'blogs'
    paginate_by = 4



class Detail_View(DetailView):
    model = Blog
    template_name = 'blog/DetailView.html'
    context_object_name = 'blog'
    # extra_context={'total_likes': Blog.total_likes(self)}

    # just overriding the function. Works fine even without the function
    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     return get_object_or_404(Blog, slug=slug)

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['liked'] = liked

        save = False
        if self.object.saved.filter(id=self.request.user.id).exists():
            save=True
        context['save'] = save
        context['is_authenticated'] = request.user.is_authenticated
        return self.render_to_response(context)



class Delete_View(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog #model/queryset is same thing(equivalent)
    template_name = 'blog/DeleteView.html'
    success_url = '/myBlog'

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False


class Create_View(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = 'blog/FormView.html'
    context_object_name = 'form'
    # success_url = 'list'
    # another way to override success_url(default -- get_absolute_url)
    def get_success_url(self):
        return '/'
    # validate all the fields in forms.py
    # Another way to check
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Update_View(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = BlogForm
    template_name = 'blog/FormView.html'
    context_object_name = 'form'
    success_url = '/myBlog'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Blog, slug=slug)

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Your account has been created! You are now able to login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form':user_form, 'p_form':profile_form}
    return render(request, 'registration/profile.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! used to validate the session and password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})




class UserBlogList_View(ListView):
    model = Blog
    template_name = 'blog/userBlog_ListView.html'
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Blog.objects.filter(author=user, status="Publish").order_by('-posted_date')




class MyBlogList_View(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/myBlog_ListView.html'
    context_object_name = 'blogs'
    paginate_by = 4
    extra_context={'heading': "My Blogs"}

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Blog.objects.filter(author=user).order_by('-posted_date')



def search(request):
    query = request.GET['query']
    if len(query) > 50:
        blogs = Blog.objects.none()

    else:
        #  SQLITE PROBLEM
        # blogTitle = Blog.objects.filter(title__icontains=query)
        # blogContent = Blog.objects.filter(content__icontains=query)
        # blogs = blogTitle.union(blogContent)

        blogs = Blog.objects.filter(
                                    Q(title__icontains=query) |
                                    Q(author__username__icontains=query) |
                                    Q(content__icontains=query)
                                    )

    if blogs.count() == 0:
        messages.warning(request, f'No Results Found. Please refine your keywords')

    context = {'title' : "Search Results",
                'query' : query,
                'blogs' : blogs}
    return render(request, 'blog/search.html', context)



class AddCategory_View(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'blog/AddCategoryView.html'
    context_object_name = 'form'
    # success_url = 'list'
    # another way to override success_url(default -- get_absolute_url)
    def get_success_url(self):
        return '/'


class CategoryBlog_View(ListView):
    model = Blog
    template_name = 'blog/CategoryBlogView.html'
    context_object_name = 'blogs'
    paginate_by = 4


    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Blog.objects.filter(category=category).order_by('-posted_date')

@login_required
def likeBlog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('DetailView', args=[str(blog.slug)]))

@login_required
def saveBlog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    save = False
    if blog.saved.filter(id=request.user.id).exists():
        blog.saved.remove(request.user)
        save = False
    else:
        blog.saved.add(request.user)
        save = True
    return HttpResponseRedirect(reverse('DetailView', args=[str(blog.slug)]))



class SavedListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/showSaved.html'
    context_object_name = 'blogs'
    paginate_by = 4
    extra_context={'heading': "Saved Blogs"}

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Blog.objects.filter(saved=user).order_by('-posted_date')

# def showSaved(request):
#     blogs = Blog.objects.filter(status="Publish").order_by('-posted_date')
#     context = {'blogs': blogs, 'heading': "Saved Blogs"}
#     return render(request, 'blog/showSaved.html',context)



def index(request):
    blogs = Blog.objects.filter(status="Publish").order_by('-posted_date')
    categories = Category.objects.all()[:6]

    paginator = Paginator(blogs,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'blogs': blogs,
                'categories' : categories,
                'page_obj':page_obj}
    return render(request, 'blog/index.html',context)



#
# def listing(request):
#     contact_list = Contact.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'list.html', {'page_obj': page_obj})








"""
FUNCTION-BASED VIEWS

def ListView(request):
    blogs = Blog.objects.all()
    context = {'blogs':blogs}
    return render(request, 'blog/ListView.html',context)

def CreateView(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ListView')
        else:
            context ={'form':form}
            return render(request, 'blog/CreateView.html',context)
    form = BlogForm()
    context = {'form':form}
    return render(request, 'blog/CreateView.html',context)
"""
