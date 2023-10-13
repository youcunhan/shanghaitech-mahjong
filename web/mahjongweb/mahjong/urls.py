from django.urls import path

from . import views

app_name = "mahjong"
urlpatterns = [
    path("", views.index, name="index"),
    path("statistics", views.statistics, name="statistics"),
    path("statistics/", views.statistics, name="statistics"),
    path("user/<str:name>", views.user, name="user"),
    path("user/<str:name>/", views.user, name="user"),
    path("userid/<int:qqnumber>", views.user_id, name="user"),
    path("userid/<int:qqnumber>/", views.user_id, name="user"),
    path("user", views.users, name="user"),
    path("user/", views.users, name="user"),
    path("rival/<str:name>", views.rival, name="rival"),
    path("rival/<str:name>/", views.rival, name="rival"),
    path("help", views.help, name="help"),
    path("help/", views.help, name="help"),
    path("majsoul_contest", views.majsoul_contest, name="majsoul_contest"),
    path("majsoul_contest/", views.majsoul_contest, name="majsoul_contest"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
