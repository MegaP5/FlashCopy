import json


def r_conj(word):

    with open('app_data/verb_maker/japanese/data.json', encoding="utf8") as json_file:
        conj = json.load(json_file)


    hiragana = ['ぁ', 'あ', 'ぃ', 'い', 'ぅ', 'う', 'ぇ', 'え', 'ぉ', 
    'お', 'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご', 
    'さ', 'ざ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'た', 
    'だ', 'ち', 'ぢ', 'っ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 
    'に', 'ぬ', 'ね', 'の', 'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 
    'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ま', 'み', 'む', 
    'め', 'も', 'ゃ', 'や', 'ゅ', 'ゆ', 'ょ', 'よ', 'ら', 'り', 'る', 
    'れ', 'ろ', 'ゎ', 'わ', 'ゐ', 'ゑ', 'を', 'ん', 'ゔ', 'ゕ', 'ゖ', 
    'ゝ', 'ゞ']

    hir = ""
    kanji = ""


    word_l = len(word) - 1

    for x in range(word_l,-1,-1):
        if word[x] in hiragana:
            hir = word[x] + hir
        else:
            for b in range(0, x + 1):
                kanji = kanji + word[b]
            break

    words = []


    for x in conj:    
        if x[0] == hir:
            for y in x[1]:            
                words.append(kanji + y)

    if not kanji + hir in words:
        words.append(kanji + hir)
    
    return words[0]