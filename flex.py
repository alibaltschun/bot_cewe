import numpy as np

from linebot.models import (
    BubbleContainer 
)

def flex_rated(title,url_img,list_voter):
    voter = [__flex_voter__(x[0],x[1].replace(",",", ")) for x in list_voter]
    flex = __flex_body__(title,url_img,voter,list_voter)
    return BubbleContainer(**flex)
    
def __flex_body__(title,url,voter,list_voter):
    
    votes = [i[0] for i in list_voter]
    
    flex = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "",
        "size": "full",
        "aspectRatio": "2:3",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "",
            "weight": "bold",
            "size": "xl"
          }
        ]
      }
    }
    
    flex['body']['contents'][0]['text'] = "ID cewe : {}".format(title)
    flex['body']['contents'].append(__flex_start__(np.mean(votes)))
    flex['hero']['url'] = url
    
    if voter != []:
        array_voter = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
            ]}
        array_voter['contents'] = voter
        flex['body']['contents'].append(array_voter)
    
    return flex

def __flex_start__(score):
    gold = {
            "type": "icon",
            "size": "sm",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          }
    grey = {
            "type": "icon",
            "size": "sm",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
          }
    score_dict = {
            "type": "text",
            "text": str(score/2),
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0
          }
    start= {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [       
        ]
      }
    
    golds = int(score/2)
    greys = int(5 - golds - (score % 2))
    half = (score % 2)/2
    greys = greys + 1 if half > 0.4 and half < 1.0 else greys
    [start['contents'].append(gold) for g in range(golds)]
    [start['contents'].append(grey) for g in range(greys)]
    start['contents'].append(score_dict)
    
    return start
      
def __flex_voter__(score,names):
    voter={
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
    voter['contents'][0]['text'] = str(score)
    voter['contents'][1]['text'] = names
    return voter

