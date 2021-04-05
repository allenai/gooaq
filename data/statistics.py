import json


one_grams = {}
total = 0
with open("qoogle.jsonl") as f:
    starting_1_word = {}
    starting_2_words = {}
    starting_3_words = {}
    starting_4_words = {}
    starting_5_words = {}
    starting_6_words = {}
    word_length = {}
    for line in f.readlines():
        json_line = json.loads(line)
        if json_line['answer'] or json_line['short_answer']:
            total +=1
            question = json_line['question']
            question_split = question.replace("?", "").split(" ")
            len1 = len(question_split)
            if len1 not in word_length:
                word_length[len1] = 0
            word_length[len1] += 1
            one_word = question_split[0]
            two_words = "//".join(question_split[0:2])
            three_words = "//".join(question_split[0:3])
            four_words = "//".join(question_split[0:4])
            five_words = "//".join(question_split[0:5])
            six_words = "//".join(question_split[0:6])
            if one_word not in starting_1_word:
                starting_1_word[one_word] = 0
            if two_words not in starting_2_words:
                starting_2_words[two_words] = 0
            if three_words not in starting_3_words:
                starting_3_words[three_words] = 0
            if four_words not in starting_4_words:
                starting_4_words[four_words] = 0
            if five_words not in starting_5_words:
                starting_5_words[five_words] = 0
            if six_words not in starting_6_words:
                starting_6_words[six_words] = 0

            starting_1_word[one_word] += 1
            starting_2_words[two_words] += 1
            starting_3_words[three_words] += 1
            starting_4_words[four_words] += 1
            starting_5_words[five_words] += 1
            starting_6_words[six_words] += 1
            for x in question_split:
                if x not in one_grams:
                    one_grams[x] = 0
                one_grams[x] +=1

starting_1_word = list(starting_1_word.items())
starting_1_word = sorted(starting_1_word, key=lambda x: -x[1])
starting_2_words = list(starting_2_words.items())
starting_2_words = sorted(starting_2_words, key=lambda x: -x[1])
starting_3_words = list(starting_3_words.items())
starting_3_words = sorted(starting_3_words, key=lambda x: -x[1])
starting_4_words = list(starting_4_words.items())
starting_4_words = sorted(starting_4_words, key=lambda x: -x[1])
starting_5_words = list(starting_5_words.items())
starting_5_words = sorted(starting_5_words, key=lambda x: -x[1])
starting_6_words = list(starting_6_words.items())
starting_6_words = sorted(starting_6_words, key=lambda x: -x[1])
one_grams = list(one_grams.items())
one_grams = sorted(one_grams, key=lambda x: -x[1])
word_length = list(word_length.items())
word_length = sorted(word_length, key=lambda x: x[0])

print(starting_1_word[:40])
print("------")
print(starting_2_words[:40])
print("------")
print(starting_3_words[:40])
print("------")
print(starting_4_words[:40])
print("------")
print(starting_5_words[:40])
print("------")
print(starting_6_words[:40])
print("------")
print(one_grams[:40])
print(total)
print("------")
print(word_length)



