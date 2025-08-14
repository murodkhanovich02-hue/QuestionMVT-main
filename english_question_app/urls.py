from django.urls import path
from .views import question_view, home_page, submit_answers, login_page_view, add_question, delete_question, update_question, logout_view, admin_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('login_page/', login_page_view, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('question_add/', add_question, name='question_add'),
    path('delete/<int:question_id>/', delete_question, name='delete_question'),
    path('update/<int:question_id>/', update_question, name='update_question'),

    path('admin_page/', admin_page, name='admin_page'),
    path('question/', question_view, name='question_view'),
    path('submit/', submit_answers, name='submit_answers'),
]
