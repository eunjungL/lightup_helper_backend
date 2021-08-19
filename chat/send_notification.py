from pyfcm import FCMNotification

APIKey = "AAAA5_P06TA:APA91bHWs9LZLi2_yu4Pqxr2RyzEbAToDyyvpoxm_eeEzUTTBr7wyDMwpAQUvrLQesTg6bU-T7fN263ww4mPrDD7Ya1OuEDQKcyLG4ETdJt5ZaN_oHrUSHVT3NGw2iaERn8EYyDhs2b6"

push_service = FCMNotification(APIKey)


def send_noti(receive_user, send_user, context):
    data_message = {
        "contents": context,
        "title": "%s에게서 새로운 메시지가 왔습니다." % send_user
    }

    result = push_service.notify_topic_subscribers(topic_name=receive_user, data_message=data_message)

    print(result)