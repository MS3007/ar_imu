from django.contrib import admin
from .models import UserInfo,UserProgressRecord,SchoolCulturl,CampusLocation,Product,UserRedemptionLog,Feedback

admin.site.site_header = "AR-IMU后台管理系统"
admin.site.site_title = "AR-IMU后台管理系统"

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ( 'nickname','wx_openid','registration_time','last_login_time','avatar')
    search_fields = ('nickname','wx_openid')
    empty_value_display = "-empty-"

class UserProgressRecordadmin(admin.ModelAdmin):
    list_display = ( 'display_nickname','get_wx_openid', 'points')
    def display_nickname(self, obj):
        return obj.wx_openid.nickname  # 返回相关的UserInfo对象的昵称
    def get_wx_openid(self, obj):
        return obj.wx_openid.wx_openid if obj.wx_openid else ''
    display_nickname.short_description = '昵称'  # 自定义列标题
    get_wx_openid.short_description = '微信登录openid'
    empty_value_display = "-empty-"

class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'radius', 'description', 'image')
    empty_value_display = "-empty-"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name','price','stock','description','image')
    empty_value_display = "-empty-"

class UserRedemptionLogAdmin(admin.ModelAdmin):
    list_display = ('display_nickname','get_wx_openid','redemption_date','product','points_spent','redemption_method')
    empty_value_display = "-empty-"
    search_fields = ('wx_openid__wx_openid',)
    list_filter = ('redemption_date', 'product')
    def display_nickname(self, obj):
        return obj.wx_openid.nickname  # 返回相关的UserInfo对象的昵称
    def get_wx_openid(self, obj):
        return obj.wx_openid.wx_openid if obj.wx_openid else ''
    display_nickname.short_description = '昵称'  # 自定义列标题
    get_wx_openid.short_description = '微信登录openid'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('display_nickname','get_wx_openid','message','timestamp')
    def display_nickname(self, obj):
        return obj.wx_openid.nickname  # 返回相关的UserInfo对象的昵称
    def get_wx_openid(self, obj):
        return obj.wx_openid.wx_openid if obj.wx_openid else ''
    display_nickname.short_description = '昵称'  # 自定义列标题
    get_wx_openid.short_description = '微信登录openid'

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserProgressRecord,UserProgressRecordadmin)
admin.site.register(CampusLocation,CampusLocationAdmin)
admin.site.register(SchoolCulturl)
admin.site.register(Product,ProductAdmin)
admin.site.register(UserRedemptionLog,UserRedemptionLogAdmin)
admin.site.register(Feedback,FeedbackAdmin)