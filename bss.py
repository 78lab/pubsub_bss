import os
import json
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import googleapiclient.discovery

load_dotenv(verbose=True)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
print('GOOGLE_APPLICATION_CREDENTIALS :' + GOOGLE_APPLICATION_CREDENTIALS)
print('SERVICE_ACCOUNT_FILE :' + SERVICE_ACCOUNT_FILE)

# TODO(developer)
# project_id = "geometric-edge-659" #firebase-relaystory
# topic_id = "play-noti"
# subs_id = "play-subs"
# publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path(project_id, topic_id)

# topic = publisher.create_topic(request={"name": topic_path})

# print("Created topic: {}".format(topic.name))
# 
# 
# 



SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
# SERVICE_ACCOUNT_FILE = '/path/to/service.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

androidpublisher = googleapiclient.discovery.build('androidpublisher', 'v3', credentials=credentials)

# packageName="com.lab78.BabySootherSeal"
# subscriptionId="pro_subs_15"
# purchaseToken="ghfihlhbeibmodjmaiooehii.AO-J1OzgKLfLWuN49wBns0uxcuap-s_5B-aTGtLctJcmu6yy47ibU9GFBvM4iiLLmGnYT6gm48NZBL57NLNqX3gDakpzte_its59QmOv6tqiLPkQJjbpkTM"

# packageName="com.lab78.BabySootherSEALFree"
# subscriptionId="pro_subs_15"
# purchaseToken="kejojkbhnoclghgkchdngafn.AO-J1OzNlcz4AShjEJY2ikXXT3ZqZlh1osOixkQdOWMHosJFw4uhwr8McjQarC0qsPbiIUt4eZJk-iYFLxqIgFZCHpUe9NY9G3BwaV00Ywzm-qraif5i8Z4"


CANJOB = 1

topic_name = "projects/geometric-edge-659/topics/play-noti"
subscription_name = "projects/geometric-edge-659/subscriptions/play-subs"

subscriber = pubsub_v1.SubscriberClient()


# subscriber.create_subscription(
#     name=subscription_name, topic=topic_name)

def callback(message):
    global CANJOB # global variable
    print(message.data)
    print('CANJOB:'+str(CANJOB))
    # decoded_data = base64.b64decode(message.data)
    # print(decoded_data)
    # decoded_data = decoded_data.decode('UTF-8')
    # print(message.data)
    decoded_data = json.loads(message.data)

    packageName = decoded_data["packageName"]  
    subscription_obj = decoded_data["subscriptionNotification"]     
    purchaseToken = subscription_obj["purchaseToken"]
    # notificationType = subscription_obj["notificationType"]
    subscriptionId = subscription_obj["subscriptionId"]

    print('packageName subscriptionId purchaseToken:' + packageName + " , " + subscriptionId + " , " + purchaseToken)

    if CANJOB == 1:
      print("canJob start!")
      CANJOB = 0
      response = androidpublisher.purchases().subscriptions().get(packageName=packageName,subscriptionId=subscriptionId,token=purchaseToken).execute()
      print(response)
      CANJOB = 1
      print("canJob end!")
    else:
      print("canJob = false")

    message.ack()



future = subscriber.subscribe(subscription_name, callback)


try:
    future.result()
except KeyboardInterrupt:
    future.cancel()


