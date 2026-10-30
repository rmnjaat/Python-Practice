from fastapi import FastAPI

from redish_client import RedisClient

app = FastAPI()

client = RedisClient("localhost" , "6379")


@app.get("/")
def health():
    user1 = client.get("user:1")
    response= client.set("user:2", "GANDU"  ,xx = True)
    response= client.set("user:2", "GANDU"  ,xx = True)
    client.expire("user:1" , 3) ## expire value

    client.set("k", "v", nx=True) ##only when not exists
    client.set("k", "v", xx=True) ##only when exists
    client.set("k", "v", get=True) ## reutrn old value
    client.set("k", "v", ex=60) ## epire after sec
    client.set("k", "v", px=60000) ##epire after nano sec
    client.set("k", "v", exat=1723200000) ##expire at ewxat time 
    client.set("k", "v", pxat=1723200000000)

    return (user1 , response)


@app.get("/List")
def List():
    client.lpush("msg" ,"Hii")

    client.ltrim("msg" ,2,10)

    return client.llen("msg")
