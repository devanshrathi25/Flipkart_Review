from flask import Flask, render_template,jsonify, request
from flask_cors import CORS, cross_origin
import pymongo
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')
@app.route('/review', methods=['POST'])
@cross_origin()
def reviews():
    searchstring = request.form['content'].replace(" ","-")
    flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()

    flipkart_html = bs(flipkartPage, "html.parser")
    bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})

    del bigboxes[0:3]  # this is just to delete unnecessary boxes
    box = bigboxes[0]
        # print(box)
    productlink = "http://www.flipkart.com" + box.div.div.div.a['href']
        # print(productlink)

    prodRes = requests.get(productlink)
    prodRes.encoding = 'utf-8'
    prod_html = bs(prodRes.text, "html.parser")
    # print(prod_html)

    commentBoxes = prod_html.findAll("div", {"class": "_3nrCtb"})

  
    reviews = []

    for commentBox in commentBoxes:
        try:
            name = commentBox.div.findAll("p", {"class": "_3LYOAd _3sxSiS"})[0].text
            # print(name)
        except:
            name = "No name"

        try:
            rating = commentBox.div.div.div.div.text
            # print(rating)
        except:
            rating = "No rating"

        try:
            commentHead = commentBox.div.div.div.p.text
            # print(comment)
        except:
            commentHead = "No comment heading"

        try:
            commentTag = commentBox.div.div.findAll("div", {"class": ""})
            comment = commentTag[0].div.text
        except:
            comment = "No comments"

        mydict = {"Product": searchstring, "Name": name, "Rating": rating, "CommentHead": commentHead,
                  "Comment": comment}


        reviews.append(mydict)

    return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])


if __name__== "__main__":
    app.run()
