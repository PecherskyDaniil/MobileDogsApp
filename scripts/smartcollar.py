import requests
import random
from datetime import datetime
import time
def start_send_requests(url,ip,dog_id):
    latitude=random.random()*30+40
    longitude=random.random()*80+40
    while(True):
        print(url+"/dogs/"+str(dog_id)+"/data?ip="+ip)
        response=requests.post(url+"/dogs/"+str(dog_id)+"/data?ip="+ip,json={"latitude":str(latitude),"longitude":str(longitude),"datetime":str(datetime.now())})
        latitude+=(random.random()/10)
        longitude+=(random.random()/10)
        time.sleep(60)