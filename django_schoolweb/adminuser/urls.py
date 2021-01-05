from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('user/<int:pindex>/', user_view),
    path('user/create/excle/', user_ecxle_create),
    path('user/delete/', user_delete),
    path('user/update/', user_update),
    path('user/role/', user_role),
    path('user/create/', user_create),

    path('new/<int:pindex>/', new_view),
    path('new/create/', new_create),
    path('new/delete/<int:id>/', new_delete),
    path('new/update/<int:id>/', new_update),
    path('new/detail/<int:id>/', new_detail),

    path('research/<int:pindex>/', research_view),
    path('research/create/', research_create),
    path('research/delete/<int:id>/', research_delete),
    path('research/update/<int:id>/', research_update),
    path('research/detail/<int:id>/', research_detail),

    path('schoolpic/<int:pindex>/', schoolpic_view),
    path('schoolpic/create/', schoolpic_create),
    path('schoolpic/delete/<int:id>/', schoolpic_delete),
    path('schoolpic/update/<int:id>/', schoolpic_update),
    path('schoolpic/detail/<int:id>/', schoolpic_detail),

    path('college/<int:pindex>/', college_view),
    path('college/create/', college_create),
    path('college/delete/<int:id>/', college_delete),
    path('college/update/<int:id>/', college_update),
    path('college/detail/<int:id>/<int:pindex>/', college_detail),

    path('major/delete/<int:id>/', major_delete),
    path('major/update/<int:id>/', major_update),
    path('major/create/<int:id>/', major_create),

    path('match/<int:pindex1>/<int:pindex2>/', match_view),
    path('match/create/', match_create),
    path('match/delete/<int:id>/', match_delete),
    path('match/updata/<int:id>/', match_updata),
    path('match/detail/<int:id>/', match_detail),
    path('match/status/<int:id>/', match_updatastatus),
    path('match/team/<int:id>/<int:pindex1>/<int:pindex2>/<int:pindex3>/', team_view),
    path('match/team/check/<int:id>/<int:ispass>/', team_check),
    path('match/result/<int:id>/', upload_matchresult),
]