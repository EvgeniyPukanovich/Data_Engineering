filename = "text_1_var_46"

with open(filename) as f:
    lines = f.readlines()

word_freq = dict()

for l in lines:
    words = (l.strip()
             .replace("!", " ")
             .replace("?", " ")
             .replace(",", " ")
             .replace(".", " ")
             .strip()).split()
    
    for w in words:
        if w in word_freq:
            word_freq[w] += 1
        else:
            word_freq[w] = 1

word_freq = dict(sorted(word_freq.items(), reverse=True, key = lambda item: item[1]))

with open("r_" + filename, "w") as f:
    for w in word_freq:
        f.write(f"{w}:{word_freq[w]}\n")
