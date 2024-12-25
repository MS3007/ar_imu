from django.shortcuts import render
from django.http import JsonResponse
from wx_api.models import CampusLocation  # 替换成你的应用程序和模型的实际名称
import math
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def map(request):
        return render(request, "map_check.html")

def haversine(lat1, lon1, lat2, lon2):#两点间距计算
    # 将经纬度从度数转换为弧度
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # 地球半径（单位：米）
    radius = 6371000.0  # 1千米 = 1000米

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance
def check_map(request):
    # 获取前端发送的数据
    pos = request.GET.get('pos')
    acc=float(request.GET.get('acc'))
    pos=pos.split(',')
    my_lat=float(pos[1])
    my_lon=float(pos[0])
    # 进行数据校验，将坐标与数据库坐标比对查询
    distance = 99999.9
    structions=CampusLocation.objects.all()
    for item in structions:
        cal_distance=haversine(float(item.latitude),float(item.longitude), my_lat, my_lon)-acc
        #print(item.name,cal_distance)
        if distance>cal_distance:
            distance=cal_distance
            name=item.name
            imgurl=item.image.url
            rad=item.radius
    if distance<=rad:
        response_data = {'status': 'success', 'message': imgurl}
    else:
        response_data = {'status': 'error', 'message': '不在打卡签到范围内哦~距离你最近的是'+name+'~'}
    return JsonResponse(response_data)