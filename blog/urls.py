from django.urls import path

from django.contrib.auth import views as auth_views

from .views import (
                Create_View,
                List_View,
                Detail_View,
                Update_View,
                Delete_View,
                UserBlogList_View,
                MyBlogList_View,
                AddCategory_View,
                CategoryBlog_View,

                index,
                register,
                profile,
                change_password,
                search,
)

urlpatterns = [
    path('create',Create_View.as_view(),name='CreateView'),
    path('list',List_View.as_view(),name='ListView'),
    path('user/<str:username>/',UserBlogList_View.as_view(),name='UserBlogView'),
    path('myBlog/',MyBlogList_View.as_view(),name='MyBlogList_View'),
    path('detail/<slug:slug>/',Detail_View.as_view(),name='DetailView'),
    path('update/<slug:slug>/',Update_View.as_view(),name='UpdateView'),
    path('delete/<slug:slug>/',Delete_View.as_view(),name='DeleteView'),
    path('add-category',AddCategory_View.as_view(),name='AddCategoryView'),
    path('category/<slug:slug>/',CategoryBlog_View.as_view(),name='CategoryBlogView'),

    path('', index, name='index'),



    path('search', search, name='search'),


    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/password_change/', change_password, name='password_change'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),


    # path('accounts/password_change_done/',
    #              auth_views.PasswordChangeDoneView.as_view(
    #                  template_name='registration/password_change_done.html'
    #              ),
    #              name='password_change_done'),

    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(
    #          template_name='users/password_reset.html'
    #      ),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='users/password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='users/password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='users/password_reset_complete.html'
    #      ),
    #      name='password_reset_complete'),

]
