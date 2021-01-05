from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class College(models.Model):
    """学院"""
    name = models.CharField(max_length=50)

    # 链接
    link = models.URLField(blank=True,null=True)

    # 联系电话
    tel = models.CharField(max_length=20,blank=True,null=True)

    # 学院简介
    content = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name



class Major(models.Model):
    """专业表"""

    name = models.CharField(max_length=100)  # 专业名

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="majors")

    def __str__(self):
        return self.name



class User(AbstractUser):
    """用户表"""
    ROLE_TYPE = (
        (3, "学生"),
        (2, "老师"),
        (1, "管理员"),
    )

    LIVETIME = (
        (0, "无期限"),
        (8, "8"),
        (7, "7"),
        (6, "6"),
        (5, "5"),
        (4, "4"),
        (3, "3"),
    )

    STATUS = (
        (0, "在读"),
        (1, "休学"),
        (2, "在职"),
        (3, "离职"),
    )

    BACKGROUND = (
        (0, "本科"),
        (1, "研究生"),
        (2, "博士"),
        (3, "博士后"),
    )
    SEX = (
        (1, "男"),
        (2, "女"),

    )

    POLITICAL_CHOICE = (
        (0, "群众"),
        (1, "共青团员"),
        (2, "中共预备党员"),
        (3, "中共党员"),
        (4, "其它党派"),

    )

    role = models.IntegerField(choices=ROLE_TYPE, default=0)

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="user",blank=True,null=True)

    # 账号期限
    livetime = models.IntegerField(choices=LIVETIME,default=6)

    # 状态
    status = models.IntegerField(choices=STATUS,default=0)

    # 入学年份
    takeschoolyear = models.IntegerField(blank=True,null=True)

    # 班级
    schoolclass = models.IntegerField(default=10000)

    # qq
    qq = models.CharField(max_length=50,default="")

    # 微信
    weixin = models.CharField(max_length=50,default="")

    # 身份证号
    idcard = models.CharField(max_length=18, default="")

    # 专业
    major = models.ForeignKey(Major,related_name="user",on_delete=models.CASCADE ,blank=True, null=True)

    # 学历
    educational_background = models.IntegerField(choices=BACKGROUND,default=0)

    # 学院
    college = models.ForeignKey(College,related_name="user",on_delete=models.CASCADE,blank=True,null=True)

    # 地址
    address = models.CharField(max_length=100,default="")

    # 头像
    head_pic = models.ImageField(max_length=1000,upload_to='avatar/%Y/%m/', verbose_name=u'头像', null=True, blank=True)

    # 登录时间
    logintime = models.DateTimeField(default=timezone.now())

    # 性别
    sex = models.IntegerField(choices=SEX,default="1")

    # 政治面貌
    political = models.IntegerField(choices=POLITICAL_CHOICE, default="1")

    # 电话
    phone = models.CharField(max_length=12,default="")


    def __str__(self):
        return self.username