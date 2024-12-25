from django.db import models

# Create your models here.

class UserInfo(models.Model):
    """ 用户表 """
    nickname = models.CharField(verbose_name="昵称", max_length=63)
    wx_openid = models.CharField(verbose_name="微信登录openid", max_length=63, primary_key=True,unique=True)
    registration_time = models.DateTimeField(verbose_name="用户注册时间",null=True, blank=True)
    last_login_time = models.DateTimeField(verbose_name="用户最后一次登录时间",null=True, blank=True)
    avatar = models.ImageField(verbose_name="用户头像",upload_to='images/UserInfo_avatar/',null=True)



    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class UserProgressRecord(models.Model):
    """ 用户积分记录表/排行榜 """
    wx_openid = models.OneToOneField(UserInfo, on_delete=models.CASCADE,verbose_name="微信登录openid")
    points = models.PositiveIntegerField(verbose_name="用户积分")

    class Meta:
        verbose_name = '用户积分数据'
        verbose_name_plural = '用户积分数据'

class SchoolCulturl(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/SchoolCulturl/')  # 指定图片上传路径


    class Meta:
        verbose_name = '校园文化数据'
        verbose_name_plural = '校园文化数据'

class CampusLocation(models.Model):
    name = models.CharField(verbose_name="地点名称", max_length=20,unique=True)
    latitude = models.DecimalField(verbose_name="纬度", max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name="经度", max_digits=9, decimal_places=6)
    description = models.TextField(verbose_name="简介", blank=True, null=True)
    radius = models.PositiveIntegerField(verbose_name="范围（米）", blank=True)
    image = models.ImageField(verbose_name="地点照片",upload_to='images/CampusLocation/')  # 指定图片上传路径


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校园标志地点'
        verbose_name_plural = '校园标志地点'

class Feedback(models.Model):
    wx_openid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="微信登录openid")
    message = models.TextField(verbose_name="反馈内容")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="反馈时间")

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = '用户反馈建议'
        verbose_name_plural = '用户反馈建议'

class Product(models.Model):
    product_name = models.CharField(verbose_name="礼品名称", max_length=100)
    description = models.TextField(verbose_name="礼品描述")
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name="库存数量")
    image = models.ImageField(upload_to='wx_api/static/img/products/', verbose_name="礼品图片", null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = '积分礼品仓库'
        verbose_name_plural = '积分礼品仓库'


class UserRedemptionLog(models.Model):
    wx_openid = models.ForeignKey(UserInfo, on_delete=models.CASCADE,verbose_name="微信登录openid")
    redemption_date = models.DateTimeField(auto_now_add=True, verbose_name="兑换时间")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="兑换礼品")
    points_spent = models.PositiveIntegerField(verbose_name="消耗积分")
    #兑换方式
    REDEMPTION_CHOICES = (
        ('1', '积分'),
        ('2', '游戏兑换'),
        ('3', '地点打卡兑换'),
        # 可以根据需要添加更多选项
    )
    redemption_method = models.CharField(
        max_length=20,
        choices=REDEMPTION_CHOICES,
        verbose_name="兑换方式"
    )
    def __str__(self):
        return f"{self.wx_openid.wx_openid} - {self.product.product_name} - {self.redemption_date}"

    class Meta:
        verbose_name = '用户积分兑换记录'
        verbose_name_plural = '用户积分兑换记录'