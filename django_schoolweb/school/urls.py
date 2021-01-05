from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('index/', index_view),
    path("repassword/",repassword_view),
    path("user/detail/",userdetail_view),
    path("user/detail/update/<int:id>/",user_update_view),
    path("user/pic/<int:id>/",userpic_update_view),
    path("major/",major_view),
    path("user/lost/<int:pindex1>/<int:pindex2>/", userlost_view),
    path("lost/<int:pindex1>/<int:pindex2>/", lost_view),
    path("lost/create/<int:type>/", lost_create_view),
    path("lost/detail/<int:id>/", lost_detail_view),
    path("user/lost/delete/<int:id>/",userlost_delete_view),
    path("user/teacher/class/<int:pindex>/",schoolsubject_teacher_view),
    path("user/student/class/<int:pindex>/",schoolsubject_student_view),
    path("user/class/create/",schoolsubject_create_view),
    path("user/class/delete/<int:id>/",subject_delete_view),
    path("user/student/class/",subject_delete_view),
    path("user/student/choiceclass/", choice_subject),
    path("user/student/deleteclass/", deletechoice_subject),
    path("user/student/deleteclass/", deletechoice_subject),
    path("user/student/score/<int:pindex>/", student_get_scroe),
    path("user/teacher/score/<int:pindex>/", subject_score_view),
    path("user/teacher/savescore/<int:id>/", save_scroe),
    path('new/detail/<int:id>/', new_detail_view),
    path('new/<int:pindex>/', new_view),
    path('research/detail/<int:id>/', research_detail_view),
    path('research/<int:pindex>/', research_view),
    path("lost/search/<int:pindex>/",lost_find_view),
    path("search/",search_view),

    path('match/<int:pindex1>/<int:pindex2>/<int:pindex3>/<int:pindex4>/', match_view),
    path('match/detail/<int:id>/', match_detail),
    path('match/search/<int:pindex>/', match_search),
    path('user/match/<int:pindex>/', user_match),
    path('user/match/sign/<int:id>/<int:pindex>/', user_sign_match),
    path('user/team/<int:pindex>/', user_team),
    path('user/team/detail/<int:id>/', user_team_detail),
    path('user/team/delete/<int:id>/', user_deletesign),
    path('user/team/updata/<int:id>/', user_updatasign),
]