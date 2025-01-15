from django.urls import path
from . import views
from .views import ArticleCreateView, ArticleUpdateView
from .views import submit_article

urlpatterns = [

   path('', views.home_dashboard, name='home_dashboard'),

    # Article form submission steps (Page 1 and Page 2)
    path('submit/page1/', views.article_form_page1, name='article_form_page1'),
    path('submit/page2/', views.article_form_page2, name='article_form_page2'),

    # Article listing and detail view
    path('articles/', views.article_list, name='article_list'),  # List all articles
    # path('articles/article_list/', views.article_list, name='article_list'),  # Alternative (can remove if not needed)
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),  # View individual article details
  

    # Dashboard views for different user roles
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('editor_dashboard/', views.editor_dashboard, name='editor_dashboard'),
    path('journalist_dashboard/', views.journalist_dashboard, name='journalist_dashboard'),
    

   
    
    # User authentication
    path('login/', views.login, name='login'),

    # Article submission for journalists
    path('submit/', views.submit_article, name='submit_article'),
    
    # Reviewing articles (accessible by editors)
    path('review/<int:article_id>/', views.review_article, name='review_article'),
    
    # Publishing articles (accessible by editors/admins)
    path('publish/<int:article_id>/', views.publish_article, name='publish_article'),

    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/edit/<int:pk>/', ArticleUpdateView.as_view(), name='article_edit'),
    # path('article/submit/<int:article_id>/', submit_article, name='article_submit'),

    # path('default', views.default_dashboard, name='default_dashboard'),
   
    # path('article_delete/', views.article_delete, name='article_delete'),
    path('article/<int:id>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:id>/approve/', views.review_article, name='article_approve'),
    path('article/<int:id>/publish/', views.publish_article, name='article_publish'),

    path('article/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),


     path('article/<int:id>/view/', views.article_view, name='article_view'),
    
     path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
     path('update-role/<int:user_id>/', views.update_user_role, name='update_user_role'),
     path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
  
]
