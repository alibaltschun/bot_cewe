from linebot.models import (
    BubbleContainer 
)

def flex_rated(title,url_img,list_voter):
    voter = [__flex_voter__(x[0],x[1].replace(",",", ")) for x in list_voter]
    flex = __flex_body__(title,url_img,voter)
    return BubbleContainer(**flex)
    
def __flex_body__(title,url,voter):
    flex = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "",
        "size": "full",
        "aspectRatio": "20:13",
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
          },
          {
            "type": "text",
            "text": "scored",
            "color": "#aaaaaa",
            "size": "md",
            "flex": 1
          }
        ]
      }
    }
    flex['body']['contents'][0]['text'] = "ID cewe : {}".format(title)
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

