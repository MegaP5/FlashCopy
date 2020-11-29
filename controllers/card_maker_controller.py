class CardMakerController:
    def __init__(self):
        self.front = ""
        self.back = ""
        self.tag = ""
        self.stars = ""
        self.deck = ["", ""]
        self.last_word = ""

    def s_card(self):
        front = self.front.replace('\n', '')
        back = self.back.replace('\n', '')
        tag = self.tag.replace('\n', '')

        f = open("app_data/decks/" + self.deck[0] + "/" + self.deck[1] + ".txt", "a", encoding="utf-8")
        f.write(f"{front}	<center><h1>{self.stars}</h1></center>{back}	{tag}\n")

    def inf_clean(self):
        self.front = ""
        self.back = ""
        self.tag = ""
        self.stars = ""
        self.deck = ["", ""]
