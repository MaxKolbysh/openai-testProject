import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import re
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


@app.route("/materialsname", methods=("GET", "POST"))
def materialsname():

    if request.method == "POST":
        word = request.form["word"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are construction material calculator."},
                {"role": "user", "content": "in 1  meter height and 1 meter length of 'Rigips' wall we have such components: Integra UMP-032 - 1m², Vario KM Duplex UV - 1,09 m², Vario KB 1 - 0,75 m, Rigips Nageldübel - 22 pieces, Rigips Schnellbauschraube TN - 21 pieces"},
                {"role": "assistant",
                 "content": "in 1 meter height and 2 meter length of 'Rigips' wall we have such components: Integra UMP-032 - 2m², Vario KM Duplex UV - 2,18 m², Vario KB 1 - 1,5 m, Rigips Nageldübel - 22 pieces, Rigips Schnellbauschraube TN - 33 pieces"},
                # {"role": "system", "content": "You are a helpful assistant."},
                # {"role": "user", "content": "You play a game where you need to pull out alternately sticks. Whoever pulls out the long yellow stick got 2 points, if long blue stick 3 points, if short stick 5 points. Peter pull out the long blue stick."},
                # {"role": "assistant",
                #  "content": "Peter got 3 points "},


                {"role": "user", "content": f"{word}"}
            ],
            # max_tokens=25,
            temperature=0.5


        )
        print(response)
        result = response.choices[0].message.content
        # final = re.sub('-', '👉', result, flags=re.IGNORECASE)

        return redirect(url_for("materialsname", result=result))
    result = request.args.get("result")
    # final = re.sub('word', '💬', result, flags=re.IGNORECASE)
    return render_template("materialsname.html", result=result)


@app.route("/taskdescription", methods=("GET", "POST"))
def taskdescription():

    if request.method == "POST":
        word = request.form["word"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an English teacher."},


                {"role": "user", "content": f"explain me the meaning of the word - {word}, without using this word in the answer"}
                # {"role": "user", "content": f"Translate the following English text to Russian: - {word}"}
                # {"role": "user", "content": f"who is the author of this quote :{word} ?"}
            ],
            # max_tokens=25,
            temperature=0.5


        )
        print(response)
        result = response.choices[0].message.content
        final = re.sub(f'{word}', '💬', result, flags=re.IGNORECASE)
        return redirect(url_for("taskdescription", result=final))

        # to check caps lock

        # final = result.replace("Boredom", "💬")
        print(response)
    result = request.args.get("result")
    # final = re.sub('word', '💬', result, flags=re.IGNORECASE)
    return render_template("taskdescription.html", result=result)


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
