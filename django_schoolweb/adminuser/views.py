from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from school.models import *
from django_schoolweb.settings import MEDIA_ROOT
import datetime
from utils.util import readuser_to_excle
import random
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


def generate_code():
    # 生成随机数
    return str(random.randint(1000, 9999))


def is_admin(func):
    '''身份认证装饰器，
    :param func:
    :return:
    '''

    def wrapper(request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("/admin/login/")
        return func(request, *args, **kwargs)

    return wrapper


def login_view(request):
    """登录页面"""
    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(username=username, password=password)
        if user is not None and user.role == 1:
            login(request, user)
            return redirect("/admin/user/1/")
        else:
            context = {"error": "密码或用户名错误"}
            return render(request, "admin/login.html", context=context)
    else:

        return render(request, "admin/login.html")


@login_required(login_url="/admin/login/")
@is_admin
def logout_view(request):
    """登出"""
    logout(request)
    return render(request, "admin/login.html")


# 用户管理
@login_required(login_url="/admin/login/")
@is_admin
def user_view(request, pindex):
    """用户页面"""
    if request.method == "GET":
        context = {"username": request.user.username, "menu": 4, "usertype": 1}
        role = request.GET.get("role", None)
        username = request.GET.get("username", None)
        last_name = request.GET.get("last_name", None)
        sex = request.GET.get("sex", None)
        takeschoolyear = request.GET.get("takeschoolyear", None)
        status = request.GET.get("status", None)

        filters = {}  # 查询字典

        if role != None and role != '':
            filters["role"] = int(role)
        if username != None and username != '':
            filters["username"] = username
        if last_name != None and last_name != '':
            filters["last_name"] = last_name
        if sex != None and sex != '':
            filters["sex"] = int(sex)
        if takeschoolyear != None and takeschoolyear != '':
            filters["takeschoolyear"] = int(takeschoolyear)
        if status != None and status != '':
            filters["status"] = int(status)

        users = User.objects.filter(**filters).all().order_by("role")
        paginator = Paginator(users, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        return render(request, "admin/user.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def user_ecxle_create(request):
    """excle新建用户"""
    file = request.FILES.get("users")
    url = MEDIA_ROOT + 'upload/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S.xls")
    with open(url, 'wb') as f:
        for data in file.chunks():
            f.write(data)
    users = readuser_to_excle(url)
    for user in users:
        while True:
            user["username"] = str(user["role"]) + str(user["sex"]) + str(user["takeschoolyear"])[
                                                                      2:4] + "00" + generate_code()
            if User.objects.filter(username=user["username"]).count() == 0:  # 防止重复
                break
        user["password"] = make_password("123456")
        User.objects.create(**user)

    return redirect("/admin/user/1/")


@login_required(login_url="/admin/login/")
@is_admin
def user_delete(request):
    """删除用户"""
    if request.is_ajax():
        users = request.POST.get("users").split(",")
        users = users[:-1]  # 最后一个是空值
        ret = "success"
        for user_id in users:
            try:
                user = User.objects.get(id=int(user_id))
                user.delete()
            except Exception as e:
                ret = "error"

        return JsonResponse({"ret": ret})


@login_required(login_url="/admin/login/")
@is_admin
def user_role(request):
    """修改用户权限"""
    if request.is_ajax():
        users = request.POST.get("users").split(",")
        users = users[:-1]  # 最后一个是空值

        role = request.POST.get("role", None)

        filters = {}
        if role != None and role != '':
            filters["role"] = int(role)

        ret = "success"
        for user_id in users:
            try:
                User.objects.filter(id=int(user_id)).update(**filters)
            except Exception as e:
                ret = "error"

        return JsonResponse({"ret": ret})


@login_required(login_url="/admin/login/")
@is_admin
def user_update(request):
    """修改用户"""
    if request.is_ajax():
        users = request.POST.get("users").split(",")
        users = users[:-1]  # 最后一个是空值

        role = request.POST.get("role", None)
        username = request.POST.get("username", None)
        last_name = request.POST.get("last_name", None)
        sex = request.POST.get("sex", None)
        takeschoolyear = request.POST.get("takeschoolyear", None)
        status = request.POST.get("status", None)

        filters = {}  # 查询字典

        if role != None and role != '':
            filters["role"] = int(role)
        if username != None and username != '':
            filters["username"] = username
        if last_name != None and last_name != '':
            filters["last_name"] = last_name
        if sex != None and sex != '':
            filters["sex"] = int(sex)
        if takeschoolyear != None and takeschoolyear != '':
            filters["takeschoolyear"] = int(takeschoolyear)
        if status != None and status != '':
            filters["status"] = int(status)

        ret = "success"
        for user_id in users:
            try:
                User.objects.filter(id=int(user_id)).update(**filters)
            except Exception as e:
                ret = "error"

        return JsonResponse({"ret": ret})


@login_required(login_url="/admin/login/")
@is_admin
def user_create(request):
    """创建用户"""
    if request.is_ajax():

        role = request.POST.get("role", None)
        username = request.POST.get("username", None)
        last_name = request.POST.get("last_name", None)
        sex = request.POST.get("sex", None)
        takeschoolyear = request.POST.get("takeschoolyear", None)
        status = request.POST.get("status", None)

        filters = {}  # 查询字典

        if role != None and role != '':
            filters["role"] = int(role)
        if username != None and username != '':
            filters["username"] = username
        if last_name != None and last_name != '':
            filters["last_name"] = last_name
        if sex != None and sex != '':
            filters["sex"] = int(sex)
        if takeschoolyear != None and takeschoolyear != '':
            filters["takeschoolyear"] = int(takeschoolyear)
        if status != None and status != '':
            filters["status"] = int(status)

        ret = "success"

        while True:
            filters["username"] = str(filters["role"]) + str(filters["sex"]) + str(filters["takeschoolyear"])[
                                                                               2:4] + "00" + generate_code()
            if User.objects.filter(username=filters["username"]).count() == 0:  # 防止重复
                break
        filters["password"] = make_password("123456")

        try:
            User.objects.create(**filters)
        except Exception as e:
            ret = "error"

        return JsonResponse({"ret": ret})


# 消息
@login_required(login_url="/admin/login/")
@is_admin
def new_view(request, pindex):
    """消息页面"""
    if request.method == "GET":
        context = {"username": request.user.username, "menu": 1, "usertype": 1}

        news = News.objects.filter().all().order_by("-publishtime")
        paginator = Paginator(news, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        return render(request, "admin/news.html", context=context)


@login_required(login_url="/admin/login/")
def new_create(request):
    """新增消息"""
    if request.method == "POST":
        context = {"username": request.user.username, "err": "", "usertype": 1}

        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        introduction = request.POST.get("introduction", None)
        files = request.FILES.getlist("files", [])
        pics = request.FILES.getlist("pics", [])

        if not all([title, content, introduction]):
            context["err"] = "数据不完整"
            return render(request, "admin/news.html", context=context)
        new = News.objects.create(title=title, introduction=introduction, content=content)
        for pic in pics:
            NewsPic.objects.create(news=new, url=pic, name=pic.name)
        for file in files:
            NewsFile.objects.create(news=new, url=file, name=file.name)
        return redirect("/admin/new/1/")


@login_required(login_url="/admin/login/")
@is_admin
def new_update(request, id):
    """修改消息 文件还没有做"""
    context = {}
    title = request.POST.get("title", None)
    content = request.POST.get("content", None)
    introduction = request.POST.get("introduction", None)
    files = request.FILES.get("files", [])
    pics = request.FILES.get("pics", [])
    if not all([title, content, introduction]):
        context["err"] = "数据不完整"
        context["usertype"] = 1
        return render(request, "admin/newdetail.html", context=context)
    try:
        new = News.objects.get(id=id)
        new.title = title
        new.content = content
        new.introduction = introduction
        new.save()
    except Exception as e:
        print(e)

    return redirect("/admin/new/1/")


@login_required(login_url="/admin/login/")
@is_admin
def new_delete(request, id):
    try:
        new = News.objects.get(id=id)
        new.delete()
    except Exception as e:
        return JsonResponse({"ret": "error"})
    return JsonResponse({"ret": "success"})


@login_required(login_url="/admin/login/")
@is_admin
def new_detail(request, id):
    try:
        new = News.objects.get(id=id)
    except Exception as e:
        return redirect("/admin/new/1/")

    return render(request, "admin/newdetail.html", context={"new": new, "menu": 1, "usertype": 1})


# 科研
@login_required(login_url="/admin/login/")
@is_admin
def research_view(request, pindex):
    """科研页面"""
    if request.method == "GET":
        context = {"username": request.user.username, "menu": 2, "usertype": 1}

        research = Research.objects.filter().all().order_by("-publishtime")
        paginator = Paginator(research, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        return render(request, "admin/research.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def research_create(request):
    if request.method == "POST":
        context = {"username": request.user.username, "err": "", "usertype": 1}

        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        introduction = request.POST.get("introduction", None)
        files = request.FILES.getlist("files", [])
        pics = request.FILES.getlist("pics", [])

        if not all([title, content, introduction]):
            context["err"] = "数据不完整"
            return render(request, "admin/research.html", context=context)
        research = Research.objects.create(title=title, introduction=introduction, content=content)
        for pic in pics:
            ResearchPic.objects.create(research=research, url=pic, name=pic.name)
        for file in files:
            ResearchFile.objects.create(research=research, url=file, name=file.name)
        return redirect("/admin/research/1/")


@login_required(login_url="/admin/login/")
@is_admin
def research_update(request, id):
    context = {"usertype": 1}
    title = request.POST.get("title", None)
    content = request.POST.get("content", None)
    introduction = request.POST.get("introduction", None)

    if not all([title, content, introduction]):
        context["err"] = "数据不完整"
        return render(request, "admin/researchdetail.html", context=context)
    try:
        research = Research.objects.get(id=id)
        research.title = title
        research.content = content
        research.introduction = introduction
        research.save()
    except Exception as e:
        print(e)

    return redirect("/admin/research/1/")


@login_required(login_url="/admin/login/")
@is_admin
def research_delete(request, id):
    try:
        research = Research.objects.get(id=id)
        research.delete()
    except Exception as e:
        return JsonResponse({"ret": "error"})
    return JsonResponse({"ret": "success"})


@login_required(login_url="/admin/login/")
@is_admin
def research_detail(request, id):
    try:
        research = Research.objects.get(id=id)
    except Exception as e:
        return redirect("/admin/research/1/")

    return render(request, "admin/researchdetail.html", context={"research": research, "menu": 2, "usertype": 1})


# 图片
@login_required(login_url="/admin/login/")
@is_admin
def schoolpic_view(request, pindex):
    """用户页面"""
    if request.method == "GET":
        context = {"username": request.user.username, "menu": 0, "usertype": 1}

        schoolpic = SchoolPic.objects.filter().all().order_by("-publishtime")
        paginator = Paginator(schoolpic, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        return render(request, "admin/schoolpic.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def schoolpic_create(request):
    """用户页面"""
    if request.method == "POST":
        context = {"username": request.user.username, "err": "", "usertype": 1}

        content = request.POST.get("content", None)
        file = request.FILES.get("pic", "")

        SchoolPic.objects.create(url=file, content=content)

        return redirect("/admin/schoolpic/1/")


@login_required(login_url="/admin/login/")
@is_admin
def schoolpic_update(request, id):
    content = request.POST.get("content", " ")
    pic = request.FILES.get("pic", "")
    print(pic)
    try:
        schoolpic = SchoolPic.objects.get(id=id)
        schoolpic.content = content
        if pic != "":
            schoolpic.url = pic
        schoolpic.save()
    except Exception as e:
        print(e)

    return redirect("/admin/schoolpic/1/")


@login_required(login_url="/admin/login/")
@is_admin
def schoolpic_delete(request, id):
    try:
        schoolpic = SchoolPic.objects.get(id=id)
        schoolpic.delete()
    except Exception as e:
        return JsonResponse({"ret": "error"})
    return JsonResponse({"ret": "success"})


@login_required(login_url="/admin/login/")
@is_admin
def schoolpic_detail(request, id):
    try:
        schoolpic = SchoolPic.objects.get(id=id)
    except Exception as e:
        return redirect("/admin/schoolpic/1/")

    return render(request, "admin/schoolpicdetail.html", context={"schoolpic": schoolpic, "menu": 0, "usertype": 1})


# 院系链接
@login_required(login_url="/admin/login/")
@is_admin
def college_view(request, pindex):
    """院系页面"""
    if request.method == "GET":
        context = {"username": request.user.username, "menu": 3, "usertype": 1}

        college = College.objects.filter().all()
        paginator = Paginator(college, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        return render(request, "admin/college.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def college_create(request):
    """院系页面"""
    if request.method == "POST":
        context = {"username": request.user.username, "err": "", "menu": 3, "usertype": 1}

        name = request.POST.get("name", None)
        content = request.POST.get("content", None)
        tel = request.POST.get("tel", None)

        if not all([tel, content, name]):
            context["err"] = "数据不完整"
            return render(request, "admin/college.html", context=context)
        College.objects.create(name=name, tel=tel, content=content)

        return redirect("/admin/college/1/")


@login_required(login_url="/admin/login/")
@is_admin
def college_update(request, id):
    """院系页面"""
    content = request.POST.get("content", " ")
    tel = request.POST.get("tel", "")
    name = request.POST.get("name", "")

    try:
        college = College.objects.get(id=id)
        college.content = content
        college.name = name
        college.tel = tel
        college.save()
    except Exception as e:
        print(e)

    return redirect("/admin/college/1/")


@login_required(login_url="/admin/login/")
@is_admin
def college_detail(request, id, pindex):
    """院系页面"""
    try:
        college = College.objects.get(id=id)
    except Exception as e:
        return redirect("/admin/college/1/")
    context = {"college": college, "menu": 3, "usertype": 1}

    paginator = Paginator(college.majors.all(), 5)  # 分十页
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    context["page"] = page
    context["pindex"] = pindex
    context["index"] = pindex - 1

    return render(request, "admin/collegedetail.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def college_delete(request, id):
    """院系页面"""
    try:
        college = College.objects.get(id=id)
        college.delete()
    except Exception as e:
        return JsonResponse({"ret": "error"})
    return JsonResponse({"ret": "success"})


@login_required(login_url="/admin/login/")
@is_admin
def major_create(request, id):
    """创建专业"""
    name = request.POST.get("name", "")
    try:
        college = College.objects.get(id=id)
        Major.objects.create(college=college, name=name)
    except Exception as e:
        print(e)
    return redirect("/admin/college/detail/" + str(id) + "/1/")


@login_required(login_url="/admin/login/")
@is_admin
def major_update(request, id):
    """修改专业"""
    if request.is_ajax():
        name = request.POST.get("name", "")
        print(name)
        try:
            major = Major.objects.get(id=id)
            major.name = name
            major.save()
        except Exception as e:
            print(e)
            return JsonResponse({"ret": "error"})
        return JsonResponse({"ret": "success"})


@login_required(login_url="/admin/login/")
@is_admin
def major_delete(request, id):
    """院系页面"""
    try:
        major = Major.objects.get(id=id)
        major.delete()
    except Exception as e:
        return JsonResponse({"ret": "error"})
    return JsonResponse({"ret": "success"})


# 比赛主页
@login_required(login_url="/admin/login/")
@is_admin
def match_view(request, pindex1, pindex2):
    """比赛页面"""
    if request.method == "GET":

        context = {"username": request.user.username, "menu": 5, "usertype": 1}


        now_match = Match.objects.filter(status=0).all().order_by('-publishtime')
        paginator = Paginator(now_match, 10)  # 分十页
        page = paginator.page(pindex1)
        context["page1"] = page
        context["pindex1"] = pindex1


        history_match = Match.objects.filter(status=1).all().order_by('-publishtime')
        paginator = Paginator(history_match, 10)  # 分十页

        page = paginator.page(pindex2)  # 传递当前页的实例对象到前端
        context["page2"] = page
        context["pindex2"] = pindex2


        return render(request, "admin/match.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def match_create(request):
    """创建比赛"""
    if request.method == "POST":
        context = {"username": request.user.username, "err": "", "menu": 5, "usertype": 1}

        name = request.POST.get("name", None)
        content = request.POST.get("content", None)
        type = request.POST.get("type", None)
        endtime = request.POST.get("endtime", None)
        advice_team = request.POST.get('advice_team', None)
        host = request.POST.get('advice_team', None)
        abstract = request.POST.get('abstract', None)
        team_people = request.POST.get('team_people', None)
        pic = request.FILES.get("pic", None)
        files = request.FILES.getlist('files', [])


        if not all([type, content, name, endtime, advice_team, host, team_people, pic, abstract]):
            context["err"] = "数据不完整"
            return render(request, "admin/matchcreate.html", context=context)
        match = Match.objects.create(user=request.user, name=name, type=type, abstract=abstract, content=content,
                                     endtime=endtime, advice_team=advice_team, host=host, team_people=team_people,
                                     pic=pic)

        if len(files) != 0:
            for file in files:

                Match_Enclosure.objects.create(enclosure=file, match=match,name=file.name)

        return redirect("/admin/match/1/1/")
    else:
        context = {"username": request.user.username, "menu": 5, "usertype": 1}

        return render(request, "admin/matchcreate.html", context=context)




@login_required(login_url="/admin/login/")
@is_admin
def match_detail(request, id):
    """比赛详情"""
    if request.method == "POST":
        pass
    else:

        match = Match.objects.get(id=id)
        context = {"username": request.user.username, "menu": 5, "usertype": 1, "match": match}

        return render(request, "admin/matchdetail.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def match_updatastatus(request, id):
    """修改比赛状态比赛"""
    if request.method == "GET":
        print(id)
        try:
            match = Match.objects.get(id=id)
        except Exception as e:
            return JsonResponse({'ret': 'error'})
        if match.status == 0:
            match.status = 1
            match.history_time = datetime.datetime.now()
        else:
            match.status = 0
        match.save()
        return JsonResponse({'ret': 'success'})


@login_required(login_url="/admin/login/")
@is_admin
def match_delete(request, id):
    """删除比赛"""
    if request.method == "GET":

        try:
            match = Match.objects.get(id=id)
        except Exception as e:
            return JsonResponse({'ret': 'error'})
        match.delete()

        return JsonResponse({'ret': 'success'})


@login_required(login_url="/admin/login/")
@is_admin
def match_updata(request, id):
    """修改比赛"""
    if request.method == "POST":

        match = Match.objects.get(id=id)

        name = request.POST.get("name", match.name)
        content = request.POST.get("content", match.content)
        type = request.POST.get("type", match.type)
        endtime = request.POST.get("endtime", match.endtime)
        advice_team = request.POST.get('advice_team', match.advice_team)
        host = request.POST.get('advice_team', match.host)
        abstract = request.POST.get('abstract', match.abstract)
        team_people = request.POST.get('team_people', match.team_people)
        pic = request.FILES.get("pic", match.pic)

        match.name = name
        match.type = type
        match.abstract = abstract
        match.content = content
        match.endtime = endtime
        match.advice_team = advice_team
        match.host = host
        match.team_people = team_people
        match.pic = pic
        match.save()
        context = {"username": request.user.username, "menu": 5, "usertype": 1, "match": match}
        return render(request, "admin/matchupdata.html", context=context)
    else:
        match = Match.objects.get(id=id)

        context = {"username": request.user.username, "menu": 5, "usertype": 1, "match": match,'endtime':str(match.endtime)}

        return render(request, "admin/matchupdata.html", context=context)


@login_required(login_url="/admin/login/")
@is_admin
def team_view(request, id,pindex1,pindex2,pindex3):
    """查看队伍"""
    if request.method == "GET":

        match = Match.objects.get(id=id)
        teamid = request.GET.get('teamid',None)

        wait_check_teams = Teams.objects.filter(match=match,check=0).all()
        paginator = Paginator(wait_check_teams, 10)  # 分十页
        page1 = paginator.page(pindex1)  # 传递当前页的实例对象到前端

        pass_teams = Teams.objects.filter(match=match,check=1).all()
        paginator = Paginator(pass_teams, 10)  # 分十页
        page2 = paginator.page(pindex2)  # 传递当前页的实例对象到前端

        no_pass_teams = Teams.objects.filter(match=match,check=2).all()
        paginator = Paginator(no_pass_teams, 10)  # 分十页
        page3 = paginator.page(pindex3)  # 传递当前页的实例对象到前端



        context = {"username": request.user.username, "menu": 5, "usertype": 1, "page1": page1,'page2':page2,'page3':page3,'match':match,'pindex1':pindex1,'pindex2':pindex2,'pindex3':pindex3}

        if teamid != None:
            team = Teams.objects.get(id=teamid)

            team = Team_Students.objects.filter(team=team).all()

            context['choiceteam'] = team

        return render(request, "admin/team.html", context=context)
    else:
        match = Match.objects.get(id=id)

        context = {"username": request.user.username, "menu": 5, "usertype": 1, "match": match,'endtime':str(match.endtime)}

        return render(request, "admin/team.html", context=context)

@login_required(login_url="/admin/login/")
@is_admin
def team_check(request,id,ispass):
    """审核队伍"""
    if request.method == 'GET':
        team = Teams.objects.get(id=id)

        if ispass == 1:  # 通过
            team.check = 1
            team.match.nocheck_team_num -= 1
            team.match.check_team_num += 1
        else:
            result = request.GET.get('result')
            team.check = 2
            team.no_pass = result
            team.match.nocheck_team_num -= 1
            team.match.check_team_num += 1
        team.match.save()
        team.save()
        return JsonResponse({'ret': 'success'})

@login_required(login_url="/admin/login/")
@is_admin
def upload_matchresult(request,id):
    """上传比赛结果"""
    if request.method == 'POST':
        file = request.FILES.get("file")
        match = Match.objects.get(id=id)
        match.result = file
        match.save()
        return redirect("/admin/match/1/1/")


