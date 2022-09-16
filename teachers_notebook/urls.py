from django.contrib.auth.decorators import login_required
from django.urls import path
from teachers_notebook import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('student/<int:pk>/', views.StudentDetailsView.as_view(), name="student"),
    path('password-change/',
         login_required(auth_views.PasswordChangeView.as_view()),
         name="password_change"),
    path('password-change/done/',
         login_required(auth_views.PasswordChangeDoneView.as_view()),
         name="password_change_done"),
    path('profile/',
         login_required(views.ProfileView.as_view()),
         name='profile'),
    path('password-reset/',
         login_required(auth_views.PasswordResetView.as_view()),
         name='password_reset'),
    path('password-reset/done',
         login_required(auth_views.PasswordResetDoneView.as_view()),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         login_required(auth_views.PasswordResetCompleteView.as_view()),
         name='password_reset_complete'),
    path('home/', views.HomeView.as_view(), name="home"),
    path('add-student/', views.AddStudentView.as_view(), name='add_student'),
    path('update-student/<int:pk>/',
         login_required(views.UpdateStudent.as_view()),
         name='update_student'),
    path('delete-student/<int:pk>/',
         login_required(views.DeleteStudent.as_view()),
         name='delete_student'),
    path('add-lesson/<int:pk>', views.AddLessonView.as_view(), name='add_lesson'),
    path('update-lesson/<int:pk>/',
         login_required(views.UpdateLesson.as_view()),
         name='update_lesson'),
    path('delete-lesson/<int:pk>/',
         login_required(views.DeleteLesson.as_view()),
         name='delete_lesson'),
    path('lesson-index/', views.LessonIndexView.as_view(), name='lesson_index'),

    path('', views.LandingPageView.as_view(), name='index'),

    ]

# path('register/', views.register, name='register'),

# path('lesson-index/', views.lesson_index, name='lesson_index'),