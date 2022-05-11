# openai.api_key = os.getenv("OPENAI_API_KEY")
from numpy import add
import openai
openai.api_key = "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"


def clean_response(ai_generated_response):
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

    reversed = ai_generated_response[::-1]
    
    # Clean up ending punctuation
    while reversed[0] in punctuation:
        reversed = reversed[1:]
    
    if reversed[-1] == '"':
        # Complete quotes, because GPT-3 sometimes likes to give the story with a trailing quote
        reversed[0] = '"'

    # unreverse it
    return reversed[::-1]

    
# STORYTELLING¡
def generate_prompt_storywriting(listOfWords):

    return """
        Write a short story of 100 to 150 words using these four words:
        \n1. {}\n2. {}\n3. {}\n4. {}"
        \n\n Story:""".format(
        listOfWords[0], listOfWords[1], listOfWords[2], listOfWords[3] 
    )


def generate_story(words):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=generate_prompt_storywriting(words),
        temperature=0.5,
        max_tokens=220,
        top_p=1,
        best_of=1,
        frequency_penalty=1.8,
        presence_penalty=1
    )

    story = response.choices[0].text
    story = clean_response(story)

    return story



# PARAGRAPH COMPLETION
def complete_para(firstSentence, secondSentence):


    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Complete the following paragraph with two or more sentences:\n\n {}.".format(firstSentence),
        suffix=secondSentence,
        temperature=0.8,
        max_tokens=220,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=1
    )

    generated_body = response.choices[0].text
    generated_body = clean_response(generated_body)
    
    # para = firstSentence + ' ' + generated_body + ' ' + secondSentence

    para = generated_body

    return para