import os

import requests
from flask import Flask, send_file, Response,render_template, request, redirect, url_for
from bs4 import BeautifulSoup
from model import Result

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return facts[0].getText()

def present_content(original,pig,loc):

    ohtml=f'<p style="color:blue;">{original}</p>'
    phtml=f'<p style="color:blue;">{pig}</p>'
    path=f'<a href="{loc}" style="color:blue;">{loc}</a>'

    result=Result(ohtml,phtml,path)
    return result

@app.route('/',methods=['GET', 'POST'])
def home():
    fact=get_fact()
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                             data={'input_text': f"{fact}"}, allow_redirects=False)
    loc = response.headers.get("Location")
    result = requests.get(loc)

    soup = BeautifulSoup(result.content, "html.parser")
    pig = soup.find("body").getText().split('\t')[1].strip()
    data=present_content(fact,pig,loc)

    return render_template('results.jinja2', result=data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

