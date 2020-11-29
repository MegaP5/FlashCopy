import re


z = "6持ち 運ばなかった6 4u4[456    ]45?{?+{_+7%@$ fghg hd"

removeSpecialChars = re.sub('[^A-Za-z0-9]+', '', z)

print(removeSpecialChars)


cleanString = re.sub('\W+','', z)

print(cleanString)