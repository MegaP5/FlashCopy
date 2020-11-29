import json

stars = ["☆☆☆☆☆", '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']


def f_stars(language, word):

    s_word = stars[0]

    with open('app_data/frequency/frequency_' + language + '.json', encoding="utf8") as json_file:
        frequency = json.load(json_file)

    try:
        position = frequency.index(word)
    except ValueError:      
        position = -1

    if(position >= 0 and position <= 1500):
        s_word = stars[5]

    elif(position > 1500 and position <= 5000):
        s_word = stars[4]

    elif(position > 5000 and position <= 15000):
        s_word = stars[3]

    elif(position > 15000 and position <= 30000):
        s_word = stars[2]

    elif(position > 30000):
        s_word = stars[1]
    else:
        s_word = stars[0]

    return s_word