from django.urls import path

#from . import views
from . import views
#from .views import ResultsView
app_name = 'myapp'
urlpatterns = [
    path('article/', views.articleview, name='article'),
    path('article/<int:id>',views.articlepageview,name='articlepage'),
    path('article/<int:id>/delete',views.articledelete,name='articledelete'),
    path('article/<int:id>/comment',views.commentview,name='comment'),
    path('article/<int:id>/comment/<int:bid>',views.commentpageview,name='commentpage'),
    path('login/',views.loginview,name='loginview'),
    path('login/check',views.login,name='login'),
    path('exit',views.exit,name='exit'),
    path('person/',views.person,name='person'),
    path("signup",views.signup,name="signup"),
    path("signupindex",views.signupindex,name="signupindex")
]
