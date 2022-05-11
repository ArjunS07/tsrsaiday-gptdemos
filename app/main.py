import os
from string import punctuation

from app.utils.unsafe_words import is_safe


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

        for word in words:
            if not is_safe(word):
                return render_template("index.html", redirectedByUnsafeWord = True)

        story_is_safe = False
        story = "🤔 Something went wrong. Click the clear button and try again. "



        max_tries = 5
        num_tries = 0

        while not story_is_safe and num_tries < max_tries:
            print('generating story...')

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

            story = response.choices[0].text
            story = clean_story(story)
            print(story)

            story_words = story.split()

            story_is_safe = True

            for story_word in story_words:
                if not is_safe(story_word):
                    story_is_safe = False
            
            num_tries += 1
            

        
        return render_template("index.html", anchor = "result", result = story, words = words)
        


    # result = request.args.get("result")
    return render_template("index.html")


def generate_prompt(listOfWords):

    return """
        Write a short story in 150 words or less using these four words:\n\n1.{}\n2.{}\n3.{}\n4.{}",
    """.format(
        listOfWords[0], listOfWords[1], listOfWords[2], listOfWords[3] 
    )

def clean_story(story):
    # Sometimes, GPT-3 gives a story with random punctuation at the end
    # For example, it once generated: "I was walking my dog when I saw my adversary. It was a moment of epiphany. I realized that I had been pristine." ];
    # This function removes the random punctuation at the end of the story

    punctuation = [
        '[',
        ']',
        ';',
        ',',
        '#',
        '&',
        "/",
        "/"
    ]

    reversed = story[::-1]
    
    # Clean up ending punctuation
    while reversed[0] in punctuation:
        reversed = reversed[1:]
    
    if reversed[-1] == '"':
        # Complete quotes, because GPT-3 sometimes likes to give the story with a trailing quote
        reversed[0] = '"'

    # unreverse it
    return reversed[::-1]

    

