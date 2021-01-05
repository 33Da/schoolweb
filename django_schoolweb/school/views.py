from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from adminuser.models import *
import re
from .models import *
from django.core.paginator import Paginator
import random
from django.db.models import Q


def generate_code():
    # 生成随机数
    return str(random.randint(1000, 9999))


def index_view(request):
    """首页"""
    context = {"username": request.user.username, "menu": 0}
    try:
        context["usertype"] = request.user.role
    except:
        pass

    # 用于轮播图
    schoolpic = SchoolPic.objects.filter().all().order_by("-publishtime")
    context["schoolpic"] = schoolpic[:6]

    # 获取新消息
    news = News.objects.all().order_by("-publishtime")
    context["news"] = news[:10]

    # 获取科研
    researchs = Research.objects.all().order_by("publishtime")
    context["researchs"] = researchs[:3]

    # 院系链接
    colleges = College.objects.all()
    context["colleges"] = colleges
    return render(request, "school/index.html", context=context)


def login_view(request):
    """登录页面"""
    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(username=username, password=password)
        if user is not None and user.status in (0, 2):
            login(request, user)
            context = {"username": username}
            return render(request, "school/userdetail.html", context=context)
        else:
            context = {"error": "密码或用户名错误"}
            return render(request, "school/login.html", context=context)
    else:
        return render(request, "school/login.html")


@login_required
def logout_view(request):
    """登出"""
    logout(request)
    return redirect("/index/")


@login_required
def repassword_view(request):
    """登出"""
    context = {"username": request.user.username, "error": ""}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    if request.method == "GET":
        return render(request, "school/repassword.html", context=context)
    else:
        idcard = request.POST.get("idcard")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")

        if repassword != password:
            context["error"] = "两次密码不一致"
            return render(request, "school/repassword.html", context=context)

        if request.user.idcard != idcard:
            context["error"] = "身份证信息错误"
            return render(request, "school/repassword.html", context=context)

        request.user.password = make_password(password)
        request.user.save()
        return render(request, "school/index.html", context=context)


@login_required
def userdetail_view(request):
    """显示用户"""
    college = College.objects.all()
    POLITICAL_CHOICE = ["群众", "共青团员", "中共预备党员", "中共党员", "其它党派"]
    BACKGROUND = ["本科", "研究生", "博士", "博士后"]

    context = {"username": request.user.username, "user": request.user, "college": college,
               "political": POLITICAL_CHOICE, "background": BACKGROUND, "usermenu": 0}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/userdetail.html", context=context)


@login_required
def user_update_view(request, id):
    """修改用户信息"""

    last_name = request.POST.get("last_name", "")
    major = request.POST.get("major", 1)
    schoolclass = request.POST.get("schoolclass", "")
    political = request.POST.get("political", 1)
    sex = request.POST.get("sex", 1)
    qq = request.POST.get("qq", "")
    idcard = request.POST.get("idcard", "")
    email = request.POST.get("email", "")
    weixin = request.POST.get("weixin", "")
    college = request.POST.get("college", 1)
    phone = request.POST.get("phone", "")
    address = request.POST.get("address", "")
    background = request.POST.get("background", 1)

    POLITICAL_CHOICE = ["群众", "共青团员", "中共预备党员", "中共党员", "其它党派"]
    BACKGROUND = ["本科", "研究生", "博士", "博士后"]

    context = {"username": request.user.username, "user": request.user, "college": College.objects.all(),
               "political": POLITICAL_CHOICE, "background": BACKGROUND, "usermenu": 0}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    # 手机号校验
    if phone != '':
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        if re.search(phone_pat, phone) is None:
            context["err"] = "手机号错误"
            return render(request, "school/userdetail.html", context=context)

    # 身份证号校验
    if idcard != '':
        if len(str(idcard)) != 18:
            context["err"] = "身份证错误"
            return render(request, "school/userdetail.html", context=context)

    # 校验邮箱
    if email != '':
        email_pat = re.compile(r'^\w+@(\w+.)+(com|cn|net)$')
        if re.search(email_pat, email) is None:
            context["err"] = "邮箱错误"
            return render(request, "school/userdetail.html", context=context)

    try:
        user = User.objects.get(id=id)
        user.last_name = last_name
        user.college = College.objects.get(id=int(college))
        user.email = email
        user.weixin = weixin
        user.major = Major.objects.get(id=int(major))
        user.sex = sex
        user.schoolclass = schoolclass
        user.political = political
        user.qq = qq
        user.idcard = idcard
        user.phone = phone
        user.address = address
        if user.role == 2:  # 如果是教师
            user.educational_background = background
        user.save()
    except Exception as e:
        print(e)
    return redirect("/user/detail/")


@login_required
def userpic_update_view(request, id):
    """修改用户头像"""
    head_pic = request.FILES.get("head_pic")

    try:
        user = User.objects.get(id=id)
    except Exception as e:
        return redirect("/user/detail/" + str(user.id))
    user.head_pic = head_pic
    user.save()

    return redirect("/user/detail/")


@login_required
def major_view(request):
    """获取专业"""
    if request.is_ajax():
        id = request.POST.get("p_id")

        majors = Major.objects.filter(college=id).all()
        data = []
        for major in majors:
            if major == request.user.major:
                data.append({"id": major.id, "name": major.name, "is_user": "True"})
            else:
                data.append({"id": major.id, "name": major.name, "is_user": "False"})
        return JsonResponse({"data": data})


@login_required
def userlost_view(request, pindex1, pindex2):
    """失物招领"""
    context = {"user": request.user, "username": request.user.username, "usermenu": 1}
    # 寻物启示
    lost1 = Lost.objects.filter(type=0, user=request.user).all().order_by("-publish_time")
    paginator = Paginator(lost1, 10)  # 分十页
    page_lost1 = paginator.page(pindex1)  # 传递当前页的实例对象到前端

    # 拾取启示
    lost2 = Lost.objects.filter(type=1, user=request.user).all().order_by("-publish_time")
    paginator = Paginator(lost2, 10)  # 分十页
    page_lost2 = paginator.page(pindex2)  # 传递当前页的实例对象到前端

    context["page1"] = page_lost1
    context["page2"] = page_lost2
    context["pindex1"] = pindex1
    context["pindex2"] = pindex2
    context["index1"] = pindex1 - 1
    context["index2"] = pindex2 - 1
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/userlost.html", context=context)


@login_required
def userlost_delete_view(request, id):
    """删除失物招领"""
    if request.is_ajax():
        try:
            lost = Lost.objects.get(id=id)
            lost.delete()
        except Exception as e:
            return JsonResponse({"ret": "error"})
        return JsonResponse({"ret": "success"})


def lost_view(request, pindex1, pindex2):
    """展示启示"""
    context = {"username": request.user.username, "menu": 3}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    # 寻物启示
    lost1 = Lost.objects.filter(type=0).all().order_by("-publish_time")
    paginator = Paginator(lost1, 10)  # 分十页
    page_lost1 = paginator.page(pindex1)  # 传递当前页的实例对象到前端

    # 拾取启示
    lost2 = Lost.objects.filter(type=1).all().order_by("-publish_time")
    paginator = Paginator(lost2, 10)  # 分十页
    page_lost2 = paginator.page(pindex2)  # 传递当前页的实例对象到前端

    context["page1"] = page_lost1
    context["page2"] = page_lost2
    context["pindex1"] = pindex1
    context["pindex2"] = pindex2
    # 轮播图
    lostpic = lost1[:6]
    context["lostpic"] = lostpic
    return render(request, "school/lost.html", context=context)


@login_required
def lost_create_view(request, type):
    """创建启示"""
    name = request.POST.get("name", '')
    content = request.POST.get("content", '')
    pic1 = request.FILES.get("pic1", None)
    pic2 = request.FILES.get("pic2", None)
    time = request.POST.get("time", None)
    tel = request.POST.get("tel", "")
    try:
        request.session.pop('err')
    except:
        pass
    if name == '' or content == '' or time == None or tel == '' or time == '':
        request.session['err'] = "参数不完全"
        return redirect("/user/lost/1/1/")
    Lost.objects.create(name=name, tel=tel, detail=content, pic1=pic1, pic2=pic2, type=type, time=time,
                        user=request.user)
    return redirect("/user/lost/1/1/")


def lost_detail_view(request, id):
    """寻物启示详情"""
    context = {"username": request.user.username, "menu": 3}
    try:
        context["lost"] = Lost.objects.get(id=id)
    except Exception as e:
        print(e)
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/lostdetail.html", context=context)


def lost_find_view(request, pindex):
    """搜索启示"""
    context = {"username": request.user.username, "menu": 3}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    search = request.GET.get("name", '')

    # 寻物启示
    lost = Lost.objects.filter(name__contains=search).all().order_by("-publish_time")
    length = lost.__len__()
    paginator = Paginator(lost, 10)  # 分十页
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    context["page"] = page
    context["pindex"] = pindex
    # 轮播图
    lostpic = Lost.objects.filter(type=0).all().order_by("-publish_time")[:6]
    context["lostpic"] = lostpic
    context["length"] = length
    return render(request, "school/serachlost.html", context=context)


@login_required
def schoolsubject_teacher_view(request, pindex):
    """教师课程信息"""
    subjects = Subject.objects.filter(teacher=request.user).all().order_by("-id")
    paginator = Paginator(subjects, 10)  # 分十页
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端

    college = College.objects.all()
    context = {"username": request.user.username, "page": page, "college": college, "pindex": pindex, "usermenu": 3}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/teacherclass.html", context=context)


@login_required
def schoolsubject_student_view(request, pindex):
    if request.method == "GET":
        classcode = request.GET.get("classcode")
        type = request.GET.get("type")
        read_type = request.GET.get("read_type")

        filters = {}
        if classcode != "" and classcode != None:
            try:
                filters["code"] = int(classcode)
            except Exception as e:
                filters["name"] = classcode
        if type != "0" and type != None:
            filters["type"] = type
        if read_type != "0" and read_type != None:
            filters["readtype"] = read_type

        subjects = Subject.objects.filter(**filters).all().order_by("-id")
        paginator = Paginator(subjects, 10)  # 分十页
        page = paginator.page(pindex)  # 传递当前页的实例对象到前端

        mychoices = UserAndSubject.objects.filter(student=request.user).all()
        mysubject = [mychoice.subject.id for mychoice in mychoices]

        context = {"username": request.user.username, "page": page, "pindex": pindex, "mysubject": mysubject,
                   "usermenu": 4}
        try:
            context["usertype"] = request.user.role
        except:
            pass
        return render(request, "school/studentsubject.html", context=context)


@login_required
def schoolsubject_create_view(request):
    """录取课程"""
    if request.method == "POST":
        name = request.POST.get("name", "")
        total = request.POST.get("total", "")
        starttime = request.POST.get("starttime", "")
        endtime = request.POST.get("endtime", "")
        type = request.POST.get("type", "")
        read_type = request.POST.get("read_type", "")
        college = request.POST.get("college", "")
        content = request.POST.get("content", "")
        credit = request.POST.get("credit", "")
        college = College.objects.get(id=int(college))
        teacher = request.user

        while True:
            # 学院编号  课程类型 + 修读类型 + 随机四位
            code = str(type) + str(read_type) + generate_code()
            subject = Subject.objects.filter(code=code).first()
            if subject == None:
                break
        Subject.objects.create(name=name, total=total, college=college, starttime=starttime, endtime=endtime, type=type,
                               readtype=read_type, content=content, code=code, teacher=teacher, credit=credit)

        return redirect("/user/teacher/class/1/")


@login_required
def subject_delete_view(request, id):
    """删除课程"""
    if request.is_ajax():
        try:
            subject = Subject.objects.get(id=id)
            subject.delete()
        except Exception as e:
            return JsonResponse({"ret": "error"})
        return JsonResponse({"ret": "success"})


@login_required
def choice_subject(request):
    """选课"""
    if request.is_ajax():
        sid = request.POST.get("sid")
        try:
            subject = Subject.objects.get(id=sid)
        except Exception as e:
            return JsonResponse({"ret": "error"})
        UserAndSubject.objects.create(subject=subject, student=request.user)
        return JsonResponse({"ret": "success"})


@login_required()
def deletechoice_subject(request):
    """退课"""
    if request.is_ajax():
        sid = request.POST.get("sid")
        try:
            subject = Subject.objects.get(id=int(sid))
            UserAndSubject.objects.filter(subject=subject, student=request.user).delete()
        except Exception as e:
            print(e)
            return JsonResponse({"ret": "error"})
        return JsonResponse({"ret": "success"})


@login_required
def subject_score_view(request, pindex):
    """录入成绩视图"""

    subject = request.GET.get("subject", 0)
    subjects = Subject.objects.filter(teacher=request.user).all()
    if int(subject) == 0:
        myclsss = UserAndSubject.objects.filter(subject__teacher=request.user).all()
    else:
        myclsss = UserAndSubject.objects.filter(subject__teacher=request.user, subject=subject).all()
    paginator = Paginator(myclsss, 10)  # 分十页
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端

    context = {"username": request.user.username, "pindex": pindex, "index": pindex - 1, "page": page,
               "subjects": subjects, "mysubject": int(subject), "usermenu": 2}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/teacherscroe.html", context=context)


def save_scroe(request, id):
    """录入成绩"""
    if request.is_ajax():
        usually = request.POST.get("usually")
        exam = request.POST.get("exam")
        total = request.POST.get("total")

        try:
            myclass = UserAndSubject.objects.get(id=int(id))
            myclass.usually_grade = int(usually)
            myclass.exam_grade = int(exam)
            myclass.total = int(total)
            myclass.save()
        except Exception as e:
            print(e)
            return JsonResponse({"ret": "error"})
        return JsonResponse({"ret": "success"})


def student_get_scroe(request, pindex):
    """学生查看成绩"""
    myclsss = UserAndSubject.objects.filter(student=request.user).all()
    paginator = Paginator(myclsss, 10)  # 分十页
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端

    context = {"username": request.user.username, "pindex": pindex, "index": pindex - 1, "page": page, "usermenu": 3}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/studentscore.html", context=context)


def new_detail_view(request, id):
    """消息详情"""
    try:
        new = News.objects.get(id=id)
        news = News.objects.exclude(id=id).all().order_by('-publishtime')[:6]
    except Exception as e:
        print(e)
        return render(request, "school/newdetail.html")
    context = {"username": request.user.username, "new": new, "news": news}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/newdetail.html", context=context)


def new_view(request, pindex):
    """消息"""
    if request.method == "GET":
        context = {"username": request.user.username}

        news = News.objects.filter().all().order_by("-publishtime")
        length = news.__len__()
        paginator = Paginator(news, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        context["length"] = length
        try:
            context["usertype"] = request.user.role
        except:
            pass
        return render(request, "school/new.html", context=context)


def research_detail_view(request, id):
    try:
        research = Research.objects.get(id=id)
        researches = Research.objects.exclude(id=id).all()
    except Exception as e:
        print(e)
        return render(request, "school/researchdetail.html")
    context = {"username": request.user.username, "research": research, "researches": researches}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/researchdetail.html", context=context)


def research_view(request, pindex):
    """科研"""
    if request.method == "GET":
        context = {"username": request.user.username}

        research = Research.objects.filter().all().order_by("-publishtime")
        length = research.__len__()
        paginator = Paginator(research, 10)  # 分十页

        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        context["page"] = page
        context["pindex"] = pindex
        context["index"] = pindex - 1
        context["length"] = length
        try:
            context["usertype"] = request.user.role
        except:
            pass
        return render(request, "school/research.html", context=context)


def search_view(request):
    """搜索"""
    context = {"username": request.user.username}
    try:
        context["usertype"] = request.user.role
    except:
        pass
    search = request.GET.get("search", '')
    if search == '':
        context["news"] = None
        context["researchs"] = None
        context["losts"] = None
        return render(request, "school/serach.html", context=context)
    researchs = Research.objects.filter(Q(title__contains=search) | Q(content__contains=search))
    news = News.objects.filter(Q(title__icontains=search) | Q(content__contains=search))
    losts = Lost.objects.filter(Q(name__contains=search) | Q(detail__contains=search))
    length = researchs.__len__() + news.__len__() + losts.__len__()
    if len(news.all()) == 0:
        context["news"] = None
    else:
        context["news"] = news

    if len(researchs.all()) == 0:
        context["researchs"] = None
    else:
        context["researchs"] = researchs

    if len(losts.all()) == 0:
        context["losts"] = None
    else:
        context["losts"] = losts
    context["length"] = length
    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/serach.html", context=context)



def match_view(request, pindex1, pindex2,pindex3,pindex4):
    """比赛页面"""
    context = {"user": request.user, "username": request.user.username, "usermenu": 3}

    match0 = Match.objects.filter(type=0).all().order_by("-publishtime")
    paginator = Paginator(match0, 10)  # 分十页
    page_match0 = paginator.page(pindex1)  # 传递当前页的实例对象到前端


    match1 = Match.objects.filter(type=1).all().order_by("-publishtime")
    paginator = Paginator(match1, 10)  # 分十页
    page_match1 = paginator.page(pindex2)  # 传递当前页的实例对象到前端

    match2 = Match.objects.filter(type=2).all().order_by("-publishtime")
    paginator = Paginator(match2, 10)  # 分十页
    page_match2 = paginator.page(pindex2)  # 传递当前页的实例对象到前端

    match3 = Match.objects.filter(type=3).all().order_by("-publishtime")
    paginator = Paginator(match3, 10)  # 分十页
    page_match3 = paginator.page(pindex3)  # 传递当前页的实例对象到前端

    context["page1"] = page_match0
    context["page2"] = page_match1
    context["pindex1"] = pindex1
    context["pindex2"] = pindex2
    context["index1"] = pindex1 - 1
    context["index2"] = pindex2 - 1
    context["page3"] = page_match2
    context["page4"] = page_match3
    context["pindex3"] = pindex3
    context["pindex4"] = pindex4
    context["index3"] = pindex3 - 1
    context["index4"] = pindex4 - 1


    try:
        context["usertype"] = request.user.role
    except:
        pass
    return render(request, "school/match.html", context=context)


def match_search(request,pindex):
    """比赛查询"""
    if request.method == "GET":
        context = {"username": request.user.username,'length':0,'page':[],'pindex':pindex}
        name = request.GET.get('name','')
        print(name)
        if name != "":
            match = Match.objects.filter(name__icontains=name).all()
            paginator = Paginator(match, 10)  # 分十页
            page_match = paginator.page(pindex)  # 传递当前页的实例对象到前端
            context['page'] = page_match
            context['length'] = len(match)

        return render(request, "school/matchsearch.html", context=context)



def match_detail(request, id):
    """比赛详情"""
    if request.method == "POST":
        pass
    else:
        match = Match.objects.get(id=id)

        context = {"match": match}

        return render(request, "admin/matchdetail.html", context=context)


@login_required
def user_match(request, pindex):
    """比赛列表"""

    match = Match.objects.all().order_by("-publishtime")
    paginator = Paginator(match, 10)  # 分十页
    page_match = paginator.page(pindex)  # 传递当前页的实例对象到前端

    context = {"username": request.user.username, "pindex": pindex, "page": page_match, "usermenu": 5}

    return render(request, "school/usermatch.html", context=context)

@login_required
def user_sign_match(request, id,pindex):
    """比赛报名"""
    if request.method == 'GET':
        match = Match.objects.get(id=id)

        context = {"username": request.user.username, 'match':match, "usermenu": 5,'peoplenum':match.team_people,'peoplenum_range':range(0,match.team_people),'pindex':pindex}

        return render(request, "school/usermatchsign.html", context=context)
    else: # 报名信息提交
        match = Match.objects.get(id=id)

        teamname = request.POST.get("teamname")
        usernames = request.POST.getlist("username",[])

        phones = request.POST.getlist("phone",[])
        teachername = request.POST.get("teachername")
        teacherphone = request.POST.get("teacherphone")
        captainusername = request.POST.get("captainusername",'')
        captainphone = request.POST.get("captainphone")

        teams = Teams.objects.filter(match=match).all()

        entrants = []
        try:
            if teamname == '':
                raise
            for team in teams:
                if teamname == team.name:
                    raise

            for index in range(0,len(usernames)):
                if usernames[index] != '':
                    user = User.objects.get(username=usernames[index])
                    for team in teams:
                        if user in team.students.all():
                            raise
                    entrants.append({'user': user, 'role': 1,'phone':phones[index]})


            user = User.objects.get(username=captainusername)
            for team in teams:
                if user in team.students.all():
                    raise

            entrants.append({'user':user,'role':0,'phone':captainphone})

        except Exception as e:
            print(e)
            context = {"username": request.user.username, 'match': match, "usermenu": 5, 'peoplenum': match.team_people,
                       'peoplenum_range': range(0, match.team_people), 'pindex': pindex,'err':'信息有误'}

            return render(request, "school/usermatchsign.html", context=context)

        if teachername != '':
            team = Teams.objects.create(name=teamname,match=match,teacher_name=teachername,teacher_phone=teacherphone)
        else:
            team = Teams.objects.create(name=teamname, match=match)
        match.nocheck_team_num += 1
        match.save()

        for entrant in entrants:

            Team_Students.objects.create(students=entrant['user'],team=team,role=entrant['role'],phone=entrant['phone'])

        return redirect('/user/match/1/')


@login_required
def user_team(request,pindex):
    """用户队伍"""
    if request.method == 'GET':
        search = request.GET.get('name',None)
        if search != None:
            myteams = Team_Students.objects.filter(students=request.user,team__match__name__contains=search).all()
        else:
            myteams = Team_Students.objects.filter(students=request.user).all()



        my = []
        for myteam in myteams:
            my.append(myteam)



        paginator = Paginator(my, 10)  # 分十页
        page_team = paginator.page(pindex)  # 传递当前页的实例对象到前端



        context = {"username": request.user.username, "pindex": pindex, "page": page_team, "usermenu": 6}
        return render(request, "school/userteam.html",context=context)



@login_required
def user_team_detail(request,id):
    """用户队伍"""
    if request.method == 'GET':
        team = Teams.objects.get(id=id)


        userteam = Team_Students.objects.filter(team=team).all()


        context = {"username": request.user.username, "userteam": userteam,  "usermenu": 6,'team':team}
        return render(request, "school/userteamdetail.html",context=context)

@login_required
def user_deletesign(request,id):
    """用户取消报名"""
    if request.method == 'GET':
        team = Teams.objects.get(id=id)

        teammatch.nocheck_team_num -= 1
        team.match.save()
        team.delete()


        return JsonResponse({'ret': 'success'})


@login_required
def user_updatasign(request,id):
    """用户修改报名"""
    if request.method == 'GET':
        team = Teams.objects.get(id=id)
        userteam = Team_Students.objects.filter(team=team,role=0).all()
        captain = Team_Students.objects.filter(team=team,role=1).first()
        # 还可以报多少个名
        else_input = team.match.team_people - len(userteam)

        context = {"username": request.user.username, "userteam": userteam, "usermenu": 6, 'team': team,'elesinput':range(else_input),'captain':captain}
        return render(request, "school/userupdatateam.html", context=context)
    else:
        # 修改
        oldteam = Teams.objects.get(id=id)
        match = oldteam.match



        teamname = request.POST.get("teamname")
        usernames = request.POST.getlist("username", [])

        phones = request.POST.getlist("phone", [])
        teachername = request.POST.get("teachername")
        teacherphone = request.POST.get("teacherphone")
        captainusername = request.POST.get("captainusername", '')
        captainphone = request.POST.get("captainphone")


        teams = Teams.objects.filter(match=match).exclude(id=id).all()


        entrants = []
        try:
            if teamname == '':
                raise
            for team in teams:
                if teamname == team.name:
                    raise

            for index in range(0, len(usernames)):
                if usernames[index] != '':
                    user = User.objects.get(username=usernames[index])
                    for team in teams:
                        if user in team.students.all():
                            raise
                    entrants.append({'user': user, 'role': 1, 'phone': phones[index]})

            user = User.objects.get(username=captainusername)
            for team in teams:
                if user in team.students.all():
                    raise

            entrants.append({'user': user, 'role': 0, 'phone': captainphone})

        except Exception as e:
            print(e)
            return redirect('/user/team/updata/'+str(id)+'/')
        oldteam.delete()
        if teachername != '':
            team = Teams.objects.create(name=teamname, match=match, teacher_name=teachername,
                                        teacher_phone=teacherphone)
        else:
            team = Teams.objects.create(name=teamname, match=match)
        match.nocheck_team_num += 1
        match.save()

        for entrant in entrants:
            Team_Students.objects.create(students=entrant['user'], team=team, role=entrant['role'],
                                         phone=entrant['phone'])

        return redirect('/user/team/1/')


