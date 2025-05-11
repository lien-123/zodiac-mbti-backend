from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.conf import settings
from dotenv import load_dotenv
import os
import random
from .models import Profile

# 載入 .env 檔案
load_dotenv()

# 星座判斷函式
def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    return "Unknown"

# GET 測試 API
@api_view(['GET'])
def hello_api(request):
    return Response({"message": "Hello from DRF 👋"})

# 修改後的 POST 表單提交 API，會回傳星座
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_form(request):
    name = request.data.get('name')
    birthday_str = request.data.get('birthday')
    mbti = request.data.get('mbti')  # ✅ 新增這一行

    try:
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
        zodiac_sign = get_zodiac_sign(birthday.month, birthday.day)
    except:
        return Response({"error": "生日格式錯誤"}, status=400)

    # ✅ 更新 MBTI 到對應使用者的 Profile（假設已登入且有關聯模型）
    if mbti and mbti in [
        'INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP',
        'ISTJ','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP'
    ]:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.mbti = mbti
        profile.save()

    return Response({
        "message": f"收到資料，{name} 你好，你的生日是 {birthday_str}",
        "zodiac": zodiac_sign
    })

# 註冊 API
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_horoscope(zodiac_sign):
    horoscope_templates = [
        f"今日運勢 ({zodiac_sign}):\n\n愛情：今日你會遇到一些心動的瞬間，要善於表達自己。\n事業：保持專注，你會在工作上取得不錯的進展。\n健康：今天適合休息和放鬆，不要太過勞累。",
        f"今日運勢 ({zodiac_sign}):\n\n愛情：感情方面會有新的突破，與另一半的關係進一步加深。\n事業：今天是解決問題的最佳時機，抓住機會。\n健康：注意休息，保持身體的平衡，適當的運動會有益健康。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：可能會有些小爭執，但無需過度焦慮，耐心解決即可。\n事業：工作中有不少挑戰，記得冷靜應對。\n健康：保持健康的飲食習慣，對身體有幫助。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：今日你會遇到一些心動的瞬間，要善於表達自己。事業：保持專注，你會在工作上取得不錯的進展。\n健康：今天適合休息和放鬆，不要太過勞累。",
        f"今日運勢 ({zodiac_sign}):\n\n愛情：愛情運勢較為穩定，不過要小心誤解，溝通非常重要。\n事業：今天你在工作中會受到別人的肯定，會有新的機會。\n健康：注意保持身體的活力，適當的運動能提升心情。",
        f"今日運勢 ({zodiac_sign}):\n\n愛情：可能會有些小爭執，但無需過度焦慮，耐心解決即可。\n事業：工作中有不少挑戰，記得冷靜應對。\n健康：保持健康的飲食習慣，對身體有幫助。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：今天是表達愛意的好時機，與伴侶的關係會更和諧。\n事業：工作上可能會遇到突發狀況，冷靜應對最重要。\n健康：保持良好的生活作息，運動有助於保持身體健康。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：感情生活會有新的發展，勇於表達自己，會得到對方的回應。\n事業：今天在事業方面要小心他人可能的挑戰，要做好充分準備。\n健康：適當放鬆，避免過度疲勞，心情愉快對健康有益。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：在感情方面，你可能會經歷一些小誤會，但最終能夠解開誤會。\n事業：工作上的挑戰讓你更加強大，要有信心。\n健康：保持良好的生活習慣，適當的戶外活動對健康有幫助。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：今天是表達愛意的好時機，與伴侶的關係會更和諧。\n事業：工作上可能會遇到突發狀況，冷靜應對最重要。\n健康：保持良好的生活作息，運動有助於保持身體健康。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：這一天適合重拾舊情，可能會與舊識重逢。\n事業：事業上需要全身心投入，否則會錯過一些重要機會。\n健康：多喝水，保持身體清新，注意皮膚護理。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：感情方面可能會有點波動，但這是成長的過程。\n事業：今天你會有很多創新的點子，適合提出新的計畫。\n健康：避免過度焦慮，放鬆心情對你的健康更有益。",
	    f"今日運勢 ({zodiac_sign}):\n\n愛情：今天你會發現自己對感情的需求變得更加強烈，不妨主動表達。\n事業：專注於長期目標，今天的努力會為未來鋪路。\n健康：稍微注意自己的飲食，避免過度的咖啡因攝取。"
    ]
    
    # 隨機選擇一個運勢模板
    horoscope = random.choice(horoscope_templates)
    
    return horoscope

@api_view(['POST'])
def get_daily_horoscope(request):
    zodiac_sign = request.data.get('zodiac_sign')

    if not zodiac_sign:
        return Response({"error": "星座未提供"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        horoscope = generate_horoscope(zodiac_sign)
        return Response({"horoscope": horoscope}, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mbti_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return Response({'mbti': profile.mbti})

    elif request.method == 'POST':
        mbti = request.data.get('mbti')
        if mbti and mbti in [
            'INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP',
            'ISTJ','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP'
        ]:
            profile.mbti = mbti
            profile.save()
            return Response({'message': 'MBTI 已更新'})
        else:
            return Response({'error': '無效的 MBTI 類型'}, status=status.HTTP_400_BAD_REQUEST)