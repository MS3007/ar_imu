import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from  wx_api.models import UserProgressRecord,Product,UserInfo,UserRedemptionLog,Feedback
# Create your views here.
def ranking(request):
    # 获取用户积分数据，可以根据具体需求编写查询逻辑
    user_progress_data = UserProgressRecord.objects.all()
    # 将用户积分数据转化为JSON格式
    data = [{'nickname': record.wx_openid.nickname, 'wx_openid': record.wx_openid.wx_openid, 'points': record.points} for record
            in user_progress_data]

    return JsonResponse({'user_progress_data': data})

def integralmall(request):
    method=request.GET.get('method')
    if method=="find":
        opid = request.GET.get('openid')
        user_progress_data = UserProgressRecord.objects.get(wx_openid=opid)
        data = [{'nickname': user_progress_data.wx_openid.nickname, 'wx_openid': user_progress_data.wx_openid.wx_openid, 'points': user_progress_data.points}]
        return JsonResponse({'find_data': data})
    elif method=="query":
        productlist=Product.objects.all()
        data = [
            {'id':record.id,'product_name':record.product_name,'price':record.price,'stock':record.stock,'description':record.stock,'image':record.image.url}
            for record
            in productlist]
        return JsonResponse({'product_list': data})
    elif method=="detailed":
        opid = request.GET.get('openid')
        checklog=UserRedemptionLog.objects.filter(wx_openid=opid)
        data=[{'product':record.product.product_name,'redemption_date':record.redemption_date,'points_spent':record.points_spent,'redemption_method':record.redemption_method}
              for record
              in checklog
              ]
        return JsonResponse({'RedemptionLog': data})
    elif method=="exchange":
        opid = request.GET.get('openid')
        proid=request.GET.get('proid')
        extype=request.GET.get('exchangetype')
        user_progress = UserProgressRecord.objects.get(wx_openid=opid)
        gift = Product.objects.get(id=proid)

        if extype=='1' and user_progress.points >= gift.price or extype=='2' or extype=='3':
            redemption_record = UserRedemptionLog.objects.create(
                wx_openid=user_progress.wx_openid,
                product=gift,
                points_spent=gift.price if extype=='1' else 0,
                redemption_method=extype,
            )
            # 减少礼品库存
            gift.stock -= 1
            gift.save()

            # 更新用户积分
            user_progress.points -= gift.price if extype=='1' else 0
            user_progress.save()
            data=[{'info':"SUCCESS",'points':user_progress.points}]
            return JsonResponse({'ReturnLog': data})
        else:
            data = [{'info': "ERROR"}]
            return JsonResponse({'ReturnLog': data})


def getuserinfo(request):
    opid = request.GET.get('openid')
    userinfo=UserInfo.objects.get(wx_openid=opid)
    data = [{'nickname': userinfo.nickname, 'avatar_url':userinfo.avatar.url}]
    return JsonResponse({'userinfo': data})
@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        try:
            # 获取前端提交的反馈文本
            data = json.loads(request.body)
            feedback_text = data.get('feedback_text', '')
            opid = data.get('openid', None)  # 如果需要记录用户ID的话
            useropenid = UserInfo.objects.get(wx_openid=opid)
            # 将反馈文本保存到数据库
            feedback_entry = Feedback.objects.create(
                wx_openid=useropenid,
                message=feedback_text
            )
            return JsonResponse({'message': 'Feedback submitted successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
