from django.urls import path

from apps.stack.views import *
app_name = 'stack'

urlpatterns = [
    path("",dashboard,name="index"),
    path("signup",get_signup,name="signup"),
    path("signin",get_signin,name="signin"),
    path("logout",get_logout,name="logout"),

    path("addquestion",get_question,name="addquestion"),
    path("addanswer/<int:pk>",get_answer,name="addanswer"),
    path("reply/<int:pk>",get_reply,name="reply"),


]
