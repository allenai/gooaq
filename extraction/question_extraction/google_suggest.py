import json
import random
import requests
import numpy as np
import time
from tqdm import tqdm
import re

query_patterns = [
    " who ",
    " whom ",
    " whose ",
    " what ",
    " which ",
    " when ",
    " where ",
    " why ",
    " how ",
    " should ",
    " would ",
    " wouldn’t ",
    " can ",
    " can’t ",
    " will ",
    " won’t ",
    " aren’t ",
    " do ",
    " does ",
    " has ",
    " have ",
    " am ",
    " are ",
    " is ",
    " shouldn’t ",
    " isn't ",
    " could ",
    " couldn’t ",
    " does ",
    " don’t ",
    " must ",
    " may ",
    " ought ",
    "reasons on why ",
    "reasons for ",
    "reasons to ",
    "should ",
    "shouldn't ",
    "should not ",
    "why should ",
    "why shouldn't ",
    "why should not ",
    "reasons why ",
    "good reasons why ",
    "pros and cons of ",
    "facts why ",
    "good reasons why ",
    "facts about why ",
    "arguments why ",
    "arguments on why ",
]

number_may_space = re.compile(r'\d may ')
number_may_end = re.compile(r'\d may$')
space_may_numbers = re.compile(r' may \d\d')
begin_may_numbers = re.compile(r'^may \d\d')


def query_and_return(prefix):
    time.sleep(0.3)
    r = requests.get(f"http://google.com/complete/search?client=chrome&q={prefix}")
    if r.status_code == 200:
        # save it
        content = r.content.decode("utf-8", errors='replace')
        content = json.loads(content)
        return content[1]
    else:
        return []


def crawl_questions():
    # then, augment the results
    all_results = []

    import os.path
    if os.path.isfile("questions.txt"):
        with open("questions.txt") as f:
            for line in f.readlines():
                all_results.append(line.replace("\n", ""))
    else:
        all_results = query_patterns

    past_queries = []
    for idx in tqdm(range(0, 30)):
        random.shuffle(all_results)
        for result in all_results:

            # the index at which we cut a prefix, for querying a new question
            idx_cut = idx * 3

            # find the index of the next space
            try:
                idx_cut = result.index(" ", idx_cut)
            except:
                print(f" ** skipping `{result}` because no space was found after index {idx_cut} . . .")
                continue

            if len(result) < idx_cut - 1:
                print(" ** skipping because it's too short")
                continue

            # skip is it is of the form `d may`, `may dd`, etc.
            if number_may_space.search(result) is not None:
                print(f" ** skipping because it matches the patten: {number_may_space}")
                continue

            if number_may_end.search(result) is not None:
                print(f" ** skipping because it matches the patten: {number_may_end}")
                continue

            if begin_may_numbers.search(result) is not None:
                print(f" ** skipping because it matches the patten: {begin_may_numbers}")
                continue

            if space_may_numbers.search(result) is not None:
                print(f" ** skipping because it matches the patten: {space_may_numbers}")
                continue

            prefix = result[:idx_cut + 1]

            # if prefix not in query_patterns:
            #     continue
            matching_patterns = [q for q in query_patterns if q in f" {prefix} "]
            if len(matching_patterns) == 0:
                print(f">>>> skipping: {result}")
                continue
            else:
                print(f"matching_patterns: {matching_patterns}")

            if prefix in past_queries:
                continue
            else:
                past_queries.append(prefix)

            for i in np.arange(ord('a'), 1 + ord('z')):
                prefix1 = prefix + chr(i)
                print(f" ** {prefix1}")
                output = query_and_return(prefix1)
                # all_results.extend(output)
                for out in output:
                    if len(out) < 15:
                        print(f" ----> {out}: too short, dropping it! ❌ ")
                        continue
                    if out not in all_results:
                        all_results.append(out)
                        print(f" ----> {out}: not found in the results! ✅ Adding it . . . ")
                    else:
                        print(f" ----> {out}: already have it . . . 🥱 ")
                print(len(all_results))
            all_results = list(set(all_results))
            all_results = sorted(all_results)
            f = open("questions.txt", "w")
            f.write("\n".join(all_results))
            f.close()


if __name__ == "__main__":
    crawl_questions()
