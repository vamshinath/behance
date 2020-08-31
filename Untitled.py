#!/usr/bin/env python
# coding: utf-8

# In[41]:


from selenium import webdriver
import time
from flask import Flask, render_template, flash, request
from datetime import datetime
import time,os
import pytz

# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')


app = Flask(__name__)
# In[29]:




# In[30]:


def getLinks(url):
    #scrollB(0.9)

    chrome = webdriver.Chrome('/home/intel/chromedriver')
    chrome.get(url)
    time.sleep(3.5)
    current = int(chrome.execute_script("return document.body.scrollHeight"))
    tmp=0
    while tmp <= current:
        chrome.execute_script("window.scrollTo(0, {})".format(tmp))
        time.sleep(0.029)
        current = int(chrome.execute_script("return document.body.scrollHeight"))
        tmp+=25

    unctcimgs = list(map(lambda x:x.get_attribute('src'),chrome.find_element_by_id("project-modules").find_elements_by_tag_name('img')))
    furks=[]
    for link in unctcimgs:
        splitss = link.split("project_modules/")
        furl = splitss[0]+"project_modules/source/"+"/".join(splitss[1].split("/")[1:])
        if furl not in furks:
            furks.append(furl)
    chrome.quit()

    return furks


@app.route("/getURLs",methods=['GET', 'POST'])
def checkLink():
    if request.method == "POST":
        burl = request.form['url']
        if "behance.net/gallery/" not in burl:
            return '<center><h1>Invalid url</h1></center>'

        burlID = burl.split("/gallery/")[1].split("/")[0]

        with open("users.txt",'a') as fl:
            fl.write(request.remote_addr+" "+request.headers.get('User-Agent')+" "+str(datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Kolkata')))+"\n")


        try:
            imgs =[]
            with open(burlID+".txt") as fl:
                for ln in fl:
                    imgs.append(ln[:-1])
            return render_template("images.html",urls=imgs)
        except Exception as e:
            e=0
        imgs = getLinks(burl)

        with open(burlID+".txt",'w') as fl:
            for url in imgs:
                fl.write(url+"\n")

        with open("newURL.txt",'a') as fl:
            fl.write(burl+" "+request.remote_addr+" "+request.headers.get('User-Agent')+" "+str(datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Kolkata')))+"\n")

        return render_template("images.html",urls=imgs)

    return '<center><h1>Invalid request</h1></center>'

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()



# %%
