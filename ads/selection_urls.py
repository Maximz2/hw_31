from django.urls import path
from ads import views

urlpatterns = [
    path('selection/', views.SelectionListView.as_view()),
    path('selection/<int:pk>/', views.SelectionDetailView.as_view()),
    path('selection/<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('selection/create/', views.SelectionCreateView.as_view()),
    path('selection/<int:pk>/delete/', views.SelectionDeleteView.as_view()),
]
