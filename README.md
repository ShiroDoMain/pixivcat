# pixivcat
an async pixiv toolbox

# Feature
- use async  
- high performance
- concurrency download
- raw pixiv api
  
# Useage  
- install pixivcat
- ```bash
  pip install pixivcat
  ```
- Login to pixiv using refresh token, if you don't have a pixiv refresh token, You can find the access method at [@upbit](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)  
- ```python
    from pixivcat.AppApi import AppClient
    refresh_token = "xxxxxxxxxxxxxxx" # your refresh token
    async def login():
        app = AppClient(refresh_token=refresh_token)
        async with app:
            image = app.illust_detail(99057163)
            print(image)
            #download image to path
            await image.download_origin("setu")
            # bookmark the image
            await app.illust_bookmark_add(image.id)
  ```  


# proxy  
if you want use your proxy, you can add the proxy link to the parameter
```python
app = AppClient(refresh_token=refresh_token,proxy="http://host:port")
```  
# exmaple
see [exmaple.py](https://github.com/ShiroDoMain/pixivcat/blob/master/exmaple.py)
