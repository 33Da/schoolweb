from adminuser.models import *
import datetime
from django.db import models
class Subject(models.Model):
    """课程"""
    READ_TYPE = (
        (1,"选修"),
        (2,"必修")
    )
    TYPE = (
        (1,"公共课"),
        (2,"实践课"),
        (3,"通识课")
    )

    name = models.CharField(max_length=100)  # 专业名

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="subjects")

    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="teachsubject")

    students = models.ManyToManyField(User, through="UserAndSubject", blank=True, null=True)

    # 备注
    content = models.CharField(max_length=200)

    # 开课时间
    starttime = models.DateField(blank=True,null=True)

    # 结束时间
    endtime = models.DateField(blank=True,null=True)

    # 课程代号
    code = models.IntegerField(default=0)

    # 总分
    total = models.IntegerField(default=100)

    # 修读方式
    readtype = models.IntegerField(choices=READ_TYPE,default=1)

    type = models.IntegerField(choices=TYPE,default=0)

    # 学分
    credit = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class UserAndSubject(models.Model):
    """学生课程表"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_subjects")

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # 考生成绩
    exam_grade = models.IntegerField(blank=True,null=True)

    # 平时分
    usually_grade = models.IntegerField(blank=True,null=True)

    # 总分
    total = models.IntegerField(blank=True,null=True)



class Lost(models.Model):
    """失物招领"""
    TYPE = (
        (0,"寻物启事"),
        (1,"拾取启示")
    )
    type = models.IntegerField(choices=TYPE,default=0)

    # 物品名称
    name = models.CharField(max_length=50)

    # 描述
    detail = models.TextField()

    # 联系电话
    tel = models.CharField(max_length=12,default="")

    # 图片
    pic1 = models.ImageField(upload_to='lost/%Y/%m/', verbose_name='图片', null=True, blank=True)

    pic2 = models.ImageField(upload_to='lost/%Y/%m/', verbose_name='图片', null=True, blank=True)

    # 拾取时间
    time = models.DateTimeField()

    # 发布时间
    publish_time = models.DateTimeField(auto_now=True)

    # 发布者
    user = models.ForeignKey(User,related_name="lost",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class News(models.Model):
    """消息发布"""
    # 标题
    title = models.CharField(max_length=50)

    # 简介
    introduction = models.CharField(max_length=200)

    # 内容
    content = models.TextField()

    publishtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class NewsPic(models.Model):
    """消息图片"""
    url = models.ImageField(max_length=1000, upload_to='news/pic/%Y/%m/')

    news = models.ForeignKey(News,on_delete=models.CASCADE,related_name="pics")

    name = models.CharField(max_length=100,default="")

class NewsFile(models.Model):
    """消息附件"""
    url = models.FileField(upload_to='news/file/%Y/%m/', )

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="files")

    name = models.CharField(max_length=100,default="")

class Research(models.Model):
    """科研成果"""
    # 标题
    title = models.CharField(max_length=50)

    # 简介
    introduction = models.CharField(max_length=200)

    # 内容
    content = models.TextField()

    publishtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ResearchPic(models.Model):
    """科研成果图片"""
    url = models.ImageField(max_length=1000, upload_to='research/pic/%Y/%m/')

    research = models.ForeignKey(Research,on_delete=models.CASCADE,related_name="pics")

    name = models.CharField(max_length=100,default="")


class ResearchFile(models.Model):
    """科研成果附件"""
    url = models.FileField(upload_to='research/file/%Y/%m/', )

    research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name="files")

    name = models.CharField(max_length=100,default="")


class SchoolPic(models.Model):
    """学校风景"""
    url = models.ImageField(max_length=1000, upload_to='schoolpic/%Y/%m/')

    # 内容
    content = models.CharField(max_length=100)

    # 发布时间
    publishtime = models.DateTimeField(auto_now=True)




class Match(models.Model):
    """比赛"""
    TYPE = (
        (0,"艺术类"),
        (1,"学术科技类"),
        (2,'体育类'),
        (3,"其他")
    )

    STATUS = (
        (0, "比赛进行"),
        (1, "比赛结束"),

    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')  # 发布人

    name = models.CharField(max_length=100)  # 赛事名称

    type = models.IntegerField(choices=TYPE)  # 类型

    endtime = models.DateField()   # 报名截止时间

    publishtime = models.DateTimeField(auto_now=True)  # 创建时间

    status = models.IntegerField(choices=STATUS,default=0)  # 比赛状态

    team_people = models.IntegerField(default=5)   # 队伍内上限人数

    host = models.CharField(max_length=150)   # 主办方

    abstract = models.TextField(blank=True,null=True)   # 简介

    advice_team = models.CharField(max_length=100)  # 秩序群

    content = models.TextField()   # 赛事详情

    pic = models.ImageField(max_length=1000, upload_to='match/pic/%Y/%m/',blank=True,null=True)

    check_team_num = models.IntegerField(default=0) # 已审核的队伍

    nocheck_team_num = models.IntegerField(default=0)   # 未审核数量

    result = models.FileField(upload_to='match/file/%Y/%m/',blank=True,null=True)  # 比赛结果

    history_time = models.DateField(blank=True,null=True)   # 移入时间


class Match_Enclosure(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE,related_name='Enclosure')

    enclosure = models.FileField(upload_to='match/file/%Y/%m/', blank=True, null=True)

    name = models.CharField(max_length=20,blank=True,null=True)



class Teams(models.Model):
    """队伍"""
    CHECK = (
        (0, "待审核"),
        (1, "已通过"),
        (2,"未通过")

    )
    check = models.IntegerField(choices=CHECK,default=0)

    students = models.ManyToManyField(User,through='Team_Students')

    match = models.ForeignKey(Match,on_delete=models.CASCADE,related_name='teams')

    name = models.CharField(max_length=100)  # 队伍名

    no_pass = models.CharField(max_length=150,blank=True,null=True)   # 审核不通过原因

    teacher_name = models.CharField(max_length=50, blank=True, null=True)

    teacher_phone = models.CharField(max_length=12, blank=True, null=True)




class Team_Students(models.Model):
    """学生队伍表"""
    ROLE = (
        (0,'队长'),
        (1,'队员'),
    )
    role = models.IntegerField(choices=ROLE,default=0)

    students = models.ForeignKey(User,on_delete=models.CASCADE)

    phone = models.CharField(max_length=12,blank=True,null=True)

    team = models.ForeignKey(Teams,on_delete=models.CASCADE)








