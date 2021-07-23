import json
import os
import random

from tqdm import tqdm

with open("split.json") as f:
    split_ids = json.load(f)

all_questions = {}
with open("gooaq.json") as f:
    for x in f.readlines():
        json_line = json.loads(x)
        all_questions[json_line['id']] = json_line

def create_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fout1 = open(filename, "w")
    return fout1

# create training instances with different sizes
for size in [2000, 20000, 200000, 2000000]:
    for split in ['train', 'test' , 'dev']:
        counter = {
            'collection': 0,
            'long': 0,
            'short': 0
        }
        ids = split_ids[split]
        print(f" =========== {split} ==========")
        fout1 = create_file(f"google_answers_short_answers_v6_size_{size}/{split}.tsv")
        fout2 = create_file(f"google_answers_long_answers_v6_size_{size}/{split}.tsv")
        fout3 = create_file(f"google_answers_collection_answers_v6_size_{size}/{split}.tsv")
        if split == 'train':
            ids = sorted(ids, key=lambda x: x[1])
            ids = [x[0] for x in ids] # most disssimilar instances appear first
        elif split == 'test' or split == 'dev':
            random.shuffle(ids)
        else:
            raise Exception("what?")
        for id in tqdm(ids):
            if min(counter['long'], counter['short'], counter['collection']) >= size:
                break
            x = all_questions[id]
            if x['short_answer']:
                if counter['short'] > size:
                    continue
                # we care about the following four types s
                if x['answer_type'] not in ['knowledge', 'feat_snip', 'unit_conv', 'time_conv']:
                    continue
                fout1.write(f"{x['question']}\t{x['short_answer']}\t{x['id']}\n")
                counter['short'] += 1
            if x['answer']:
                if x['answer_type'] == 'collection':
                    if counter['collection'] > size:
                        continue
                    fout3.write(f"{x['question']}\t{x['answer']}\t{x['id']}\n")
                    counter['collection'] += 1
                else:
                    if counter['long'] > size:
                        continue
                    fout2.write(f"{x['question']}\t{x['answer']}\t{x['id']}\n")
                    counter['long'] += 1