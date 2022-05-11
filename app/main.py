from crypt import methods
import os
from string import punctuation

from app.utils.unsafe_words import is_safe
from app.utils.gpt_utils import generate_story, complete_para


from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/story", methods=["GET", "POST"])
def story():
    if request.method == "POST":

        words = [
            request.form["story-prompt-1"],
            request.form["story-prompt-2"],
            request.form["story-prompt-3"],
            request.form["story-prompt-4"]
        ]

        for word in words:
            if not is_safe(word):
                return render_template("story.html", redirectedByUnsafeWord = True)

        story_is_safe = False
        story = "🤔 Something went wrong. Click the clear button and try again. "

        max_tries = 5
        num_tries = 0

        while not story_is_safe and num_tries < max_tries:
            print('generating story...')

            story = generate_story(words)

            story_words = story.split()

            story_is_safe = True

            for story_word in story_words:
                if not is_safe(story_word):
                    story_is_safe = False
            
            num_tries += 1
            
        return render_template("story.html", anchor = "result", result = story, words = words)
        
    return render_template("story.html")

@app.route("/complete", methods=["GET", "POST"])
def complete():
    if request.method == "POST":

        sentence1 = request.form["sentence-1"]
        sentence2 = request.form["sentence-2"]

        for word in list(set(sentence1.split() + sentence2.split())):
            if not is_safe(word):
                return render_template("complete.html", redirectedByUnsafeWord = True)

        para_is_safe = False
        para = "🤔 Something went wrong. Click the clear button and try again. "

        max_tries = 5
        num_tries = 0

        while not para_is_safe and num_tries < max_tries:
            print('generating para...')

            para = complete_para(sentence1, sentence2)
            para_words = para.split()

            para_is_safe = True

            for para_word in para_words:
                if not is_safe(para_word):
                    para_is_safe = False
            
            num_tries += 1
        
            

        return render_template("complete.html", anchor = "result", result = para, sentence1 = sentence1, sentence2 = sentence2)
        

    return render_template("complete.html") 