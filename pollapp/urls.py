from django.urls import path

from pollapp import views


app_name = 'pollapp'
urlpatterns = [
    path('login/', views.login, name='login'),
    # Опросы (surveys)
    path('pollapp/create/', views.survey_create, name='poll_create'),
    path('pollapp/update/<int:survey_id>/', views.survey_update, name='poll_update'),
    path('pollapp/view/', views.survey_view, name='poll_view'),
    path('pollapp/view/active/', views.active_poll_view, name='active_poll_view'),
    # Вопрос (question)
    path('question/create/', views.question_create, name='question_create'),
    path('question/update/<int:question_id>/', views.question_update, name='question_update'),
    # Выбор (choice)
    path('choice/create/', views.choice_create, name='choice_create'),
    path('choice/update/<int:choice_id>/', views.choice_update, name='choice_update'),
    # Ответ (answer)
    path('answer/create/', views.answer_create, name='answer_create'),
    path('answer/view/<int:user_id>/', views.answer_view, name='answer_view'),
    path('answer/update/<int:answer_id>/', views.answer_update, name='answer_update')

]

