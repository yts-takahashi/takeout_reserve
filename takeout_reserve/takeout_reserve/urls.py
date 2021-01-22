"""takeout_reserve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from dishes.models import Category, Dish

import json

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, CarouselTemplate,CarouselColumn,PostbackAction,MessageAction
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('x1BuyT+Guw+lawys4jlznLgLOy70jmclbxBxxlaPfZJ7S/RD15NhV8kn5QCD1ujatJ3fPZlyPYgYguHWhsdpJ72Hdg9N7ElApJDaOzvC1FGS0EGjAKtPT39by8XzWtnUk4ru0Kmk2XSTsUPHm4kYrQdB04t89/1O/w1cDnyilFU=')

@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    reply_token = sent_json['events'][0]['replyToken']
    # response = HttpResponse('''{
    #         "replyToken":"''' + reply_token + '''",
    #         "messages":[
    #             {
    #                 "type":"text",
    #                 "text":"Hello, user"
    #             }
    #         ]
    #     }''')
    # response['Content-Type'] = 'application/json'
    # response['Authorization'] = 'Bearer x1BuyT+Guw+lawys4jlznLgLOy70jmclbxBxxlaPfZJ7S/RD15NhV8kn5QCD1ujatJ3fPZlyPYgYguHWhsdpJ72Hdg9N7ElApJDaOzvC1FGS0EGjAKtPT39by8XzWtnUk4ru0Kmk2XSTsUPHm4kYrQdB04t89/1O/w1cDnyilFU='

    categories = Category.objects.all()
    columns = []
    for category in categories:
        actions = []
        for dish in category.dish_set.all():
            ma = MessageAction(
                label=dish.name,
                text=dish.name
            )
            actions.append(ma)
        cm = CarouselColumn(
                thumbnail_image_url='https://1.bp.blogspot.com/-D2I7Z7-HLGU/Xlyf7OYUi8I/AAAAAAABXq4/jZ0035aDGiE5dP3WiYhlSqhhMgGy8p7zACNcBGAsYHQ/s1600/no_image_square.jpg',
                title=category.name,
                text='description1',
                actions=actions
            )
        columns.append(cm)


    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=columns
        )
    )
    try:
        line_bot_api.reply_message(reply_token, carousel_template_message)
    except LineBotApiError as e:
        pass

    # return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', callback)
]
