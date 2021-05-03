from django.shortcuts import render, redirect, get_object_or_404

from .models import Blog
from .forms import BlogForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# DetailView/ DeleteView (similar)
# CreateView/ UpdateView (similar)

class List_View(ListView):
    queryset = Blog.objects.order_by('-date_time')
    template_name = 'blog/ListView.html'
    context_object_name = 'blogs'


class Detail_View(DetailView):
    # queryset = Blog.objects.order_by('-date_time')
    model = Blog #model/queryset is same thing(equivalent)
    template_name = 'blog/DetailView.html'
    context_object_name = 'blog'

    # just overriding the function. Works fine even without the function
    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Blog, id=id)


class Delete_View(DeleteView):
    model = Blog #model/queryset is same thing(equivalent)
    template_name = 'blog/DeleteView.html'
    success_url = '/'


class Create_View(CreateView):
    form_class = BlogForm
    template_name = 'blog/CreateView.html'
    context_object_name = 'form'
    # success_url = 'list'
    # another way to override success_url(default -- get_absolute_url)
    def get_success_url(self):
        return '/'
    # validate all the fields in forms.py
    # Another way to check
    def form_valid(self, form):
        return super().form_valid(form)


class Update_View(UpdateView):
    form_class = BlogForm
    template_name = 'blog/CreateView.html'
    context_object_name = 'form'
    success_url = '/'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Blog, id=id)




# FUNCTION-BASED VIEWS

# def ListView(request):
#     blogs = Blog.objects.all()
#     context = {'blogs':blogs}
#     return render(request, 'blog/ListView.html',context)

# def CreateView(request):
#     if request.method == 'POST':
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ListView')
#         else:
#             context ={'form':form}
#             return render(request, 'blog/CreateView.html',context)
#     form = BlogForm()
#     context = {'form':form}
#     return render(request, 'blog/CreateView.html',context)
