import requests
import json
import traceback

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from dishes.models import Category, Dish, Order, OrderDetail

import json

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, CarouselTemplate,CarouselColumn,PostbackAction,MessageAction
from linebot.exceptions import LineBotApiError

ACCESS_TOKEN = 'x1BuyT+Guw+lawys4jlznLgLOy70jmclbxBxxlaPfZJ7S/RD15NhV8kn5QCD1ujatJ3fPZlyPYgYguHWhsdpJ72Hdg9N7ElApJDaOzvC1FGS0EGjAKtPT39by8XzWtnUk4ru0Kmk2XSTsUPHm4kYrQdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(ACCESS_TOKEN)

@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    sent_message = sent_json['events'][0]['message']['text']
    reply_token = sent_json['events'][0]['replyToken']
    user_id = sent_json['events'][0]['source']['userId']

    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
    user_name = json.loads(result.text)['displayName']
    try:
        if sent_message == 'メニュー':
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

            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=columns
                )
            )
        # オーダー受付中のときのみ注文を受け付ける
        elif Dish.objects.filter(name=sent_message).first():
            dish = Dish.objects.filter(name=sent_message).first()
            order = Order.objects.filter(customer=user_id, status=0).first()
            if not order:
                order = Order(customer=user_id)
                order.save()

            order_detail = OrderDetail.objects.filter(order=order, dish__name=sent_message).first()
            if order_detail:
                order_detail.amount = order_detail.amount + 1
            else:
                order_detail = OrderDetail(order=order, dish=dish, amount=1)
            order_detail.save()

            message = TextSendMessage(text='他にご注文はありますか？')
        elif Order.objects.filter(customer=user_id, status=0).first()\
            and sent_message == '完了':
            order = Order.objects.filter(customer=user_id, status=0).first()
            if not order:
                # 新しいオーダーを作る
                order = Order(customer=user_id)
                order.save()

            order_details = order.orderdetail_set.all()
            message = TextSendMessage(text=f'{order.ordered_at:%Y年%m月%d日 %H時%M分}に注文を受け付けました。\n{output_order_details(order_details)}')
            # 注文完了
            order.status = 1
            order.save()
        else:
            message = TextSendMessage(text=f'{user_name}さん いらっしゃいませ。\n「メニュー」と送信すると、注文を開始できます。')
    except Exception:
            message = TextSendMessage(text=f'{user_name}さん いらっしゃいませ。\n「メニュー」と送信すると、注文を開始できます。')
    
            traceback.print_exc()
    line_bot_api.reply_message(reply_token, message)

def output_order_details(order_details):
    result = ''
    for order_detail in order_details:
        result += f'{order_detail.dish.name}: {order_detail.amount}個\n'
    return result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', callback)
]
