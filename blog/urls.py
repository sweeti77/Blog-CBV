from django.urls import path

from .views import (
                Create_View,
                List_View,
                Detail_View,
                Update_View,
                Delete_View,
)

urlpatterns = [
    path('create',Create_View.as_view(),name='CreateView'),
    path('',List_View.as_view(),name='ListView'),
    path('detail/<int:pk>/',Detail_View.as_view(),name='DetailView'),
    path('update/<int:pk>/',Update_View.as_view(),name='UpdateView'),
    path('delete/<int:pk>/',Delete_View.as_view(),name='DeleteView'),




]
