import json

type_merging = {
    'overview': 'knowledge',
    'knowledge': 'knowledge',
    'rich_snip': 'feat_snip',
    'feat_snip': 'feat_snip',
    'unit_conv': 'unit_conv',
    'time_conv': 'time_conv',
    'curr_conv': 'curr_conv',
    'rich_set': 'collection',
    'rich_list': 'collection',
    'no_answer': 'unknown',
    'local_rst': 'unknown',
    'descript': 'unknown',
    'tr_result': 'translation',
    'localtime': 'localtime',
    'weather': 'weather',
    'direction': 'direction',
    None: 'unknown'
}

outfile = open("qoogle.jsonl", "w")
with open("dump.json") as f:
    for x in f.readlines():
        json_x = json.loads(x)
        json_x['answer_type'] = type_merging[json_x['answer_type']]
        if json_x["short_answer"] != None and json_x["short_answer"].lower() == "give general feedback":
            json_x["short_answer"] = None

        outfile.write(json.dumps(json_x) + "\n")

