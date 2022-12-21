import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():

    return render_template("index.html")


@app.route("/namegen", methods=("GET", "POST"))
def namegen():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("namegen", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("namegen.html", result=result)

@app.route("/image", methods=("GET", "POST"))
def image():
    if request.method == "POST":
        imagedescription = request.form["imagedescription"]
        response = openai.Image.create(
            prompt=imagedescription,
            n=1,
            size="512x512"
        )
        return redirect(url_for("image", result=response['data'][0]['url']))

    result = request.args.get("result")
    return render_template("image.html", result=result)


@app.route("/textgen", methods=("GET", "POST"))
def textgen():
    if request.method == "POST":
        textbody = request.form["textbody"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=textbody,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return redirect(url_for("textgen", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("textgen.html", result=result)



def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
