import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        words = [
            request.form["story-prompt-1"],
            request.form["story-prompt-2"],
            request.form["story-prompt-3"],
            request.form["story-prompt-4"]            
        ]

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_prompt(words),
            temperature=0.3,
            max_tokens=200,
            top_p=1,
            best_of=1,
            frequency_penalty=1.25,
            presence_penalty=1
        )

        return render_template("index.html", anchor = "result", result = response.choices[0].text, words = words)


    # result = request.args.get("result")
    return render_template("index.html")


def generate_prompt(listOfWords):

    return """
        Write a short story in 100 words or less using the following four words:\n\n1.{}\n2.{}\n3.{}\n4.{}",
    """.format(
        listOfWords[0], listOfWords[1], listOfWords[2], listOfWords[3] 
    )

