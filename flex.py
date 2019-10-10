def flex_rated(url,list_voter):
    voter = [__flex_voter__(x[0],x[1]) for x in list_voter]
    flex = __flex_body__(url,voter)
    return flex
    
def __flex_body__(url,voter):
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
            "text": "Brown Cafe",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
            ]
          }
        ]
      }
    }
    flex['hero']['url'] = url
    flex['body']['contents'][1]['contents'] = voter
    
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
    voter['contents'][0]['text'] = score
    voter['contents'][1]['text'] = names
    return voter

