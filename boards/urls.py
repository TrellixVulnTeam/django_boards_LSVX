from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('boards/<int:board_id>', views.boards_topics, name='board_topics'),
    path('boards/<int:board_id>/add', views.add_topic, name='add_topic'),
    path('boards/<int:board_id>/topic/<int:topic_id>/', views.topic, name='topic'),
    path('boards/<int:board_id>/topic/<int:topic_id>/relpy', views.topic_reply, name='topic_reply'),
    path('boards/<int:board_id>/topic/<int:topic_id>/comments/<int:comment_id>/edit',
         views.PostUpdateView.as_view(),
         name='edit_comment'),
]

