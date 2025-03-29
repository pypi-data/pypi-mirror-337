import numpy as np
import math

def Sentiment(text):

    val = 0
    posi = negi = 0

    pos = [
        "excellent", "amazing", "fantastic", "great", "positive", "happy", "joyful",
        "outstanding", "brilliant", "wonderful", "superb", "spectacular", "awesome",
        "love", "like", "admire", "incredible", "successful", "satisfied", "delightful",
        "cheerful", "enthusiastic", "fabulous", "grateful", "optimistic", "thrilled",
        "impressive", "inspiring", "rewarding", "glorious", "terrific", "peaceful",
        "uplifting", "pleasant", "magnificent", "radiant", "charming", "hopeful"
    ]

    neg = [
        "terrible", "horrible", "awful", "bad", "negative", "sad", "unhappy",
        "disappointing", "frustrating", "miserable", "angry", "hate", "dislike",
        "pathetic", "dreadful", "tragic", "painful", "horrendous", "wretched",
        "unpleasant", "depressing", "gloomy", "hopeless", "dismal", "upset",
        "annoying", "devastating", "heartbreaking", "disastrous", "discouraging",
        "grief", "resentful", "regretful", "atrocious", "distressing", "mournful", "mourn"
    ]

    words = text.lower().split()

    for word in words:
        if word in pos:
            posi += 1
            val += 1
        elif word in neg:
            negi -= 1
            val -= 1

    sen = np.interp(val, (negi, posi), (-1, 1))

    factor = 10 ** 2
    sentiment = math.ceil(sen * factor) / factor

    return sentiment
