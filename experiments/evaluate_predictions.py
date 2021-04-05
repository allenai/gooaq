#!/usr/bin/env python

"""Evaluate model predictions against target.
Usage:
   evaluate_predictions.py --model_mixture_name=NAME --dataset_mixture_name=NAME --bucket_name=GOOGLE_CLOUD_BUCKET_NAME --eval_metric=METRIC_NAME [--model_size=SIZE] [--input_sequence_length=LEN] [--output_sequence_length=LEN]
   evaluate_predictions.py --eval_path=NAME --eval_metric=METRIC_NAME [--input_sequence_length=LEN] [--output_sequence_length=LEN]
   evaluate_predictions.py -h| --help
Options:
    -h --help                               Show this screen
   --model_mixture_name=NAME                Name of the model whose predictions are to be evaluated
   --dataset_mixture_name=NAME              Name of the dataset the predictions on which we want to evaluate
   --bucket_name=GOOGLE_CLOUD_BUCKET_NAME   Name of the bucket in GoogleCloud where the predictions are stored
   --eval_path=NAME                         gs:// link to predictions to evaluate
   --eval_metric=METRIC_NAME                Name of the evaluation metric. Currently recognized options: efficientqa_exact, efficientqa_regex
   --model_size=SIZE                        Size of the t5 model whose predictions are to be evaluated
"""
# example run:
# python evaluate_predictions.py --eval_path=gs://danielk-files/qoogle-t5-models/google_answers_short_answers_v6_size_2000/11B/dev_eval --eval_metric=f1

import json
import random

import efficientqa_eval_utils
from squad11_eval_utils import metric_max_over_ground_truths, f1_score, exact_match_score
from narrativeqa_eval_utils import rouge_l, metric_max_over_ground_truths_r
import re
import t5
import tensorflow.compat.v1 as tf

from docopt import docopt
from google.cloud import storage

all_questions = {}
with open("../collecting_answers/dump.json") as f:
    for x in f.readlines():
        json_line = json.loads(x)
        all_questions[json_line['id']] = json_line


def evaluate(targets, predictions, eval_metric, ids):
    score = 0
    num_examples = 0
    missing_examples = []
    per_type_scores = {
        'short_answer': [],
        'long_answer': []
    }
    questions = targets.keys()
    if len(questions) > 1000:
        questions = random.sample(questions, 1000)
    for question in questions:
        if question in predictions:
            # print("------")
            # print(question)
            # print(targets[question])
            # print(predictions[question])
            curr_score = 0
            num_examples += 1
            if eval_metric == 'efficientqa_exact':
                curr_score = int(
                    efficientqa_eval_utils.is_correct(answers=targets[question], prediction=predictions[question],
                                                      is_regex=False))
            elif eval_metric == 'efficientqa_regex':
                curr_score = int(
                    efficientqa_eval_utils.is_correct(answers=targets[question], prediction=predictions[question],
                                                      is_regex=True))
            elif eval_metric == 'f1':
                curr_score = metric_max_over_ground_truths(
                    f1_score, predictions[question], targets[question])
            elif eval_metric == 'em':
                curr_score = metric_max_over_ground_truths(
                    exact_match_score, predictions[question], targets[question])
            elif eval_metric == 'rouge':
                new_targets = []
                for target in targets[question]:
                    if "///" in target:
                        new_targets.extend(target.split("///"))
                    else:
                        new_targets.append(target)
                rouge_l_score = metric_max_over_ground_truths_r(rouge_l, predictions[question], new_targets)
                curr_score = rouge_l_score["rouge-l"]["f"]
            if ids:
                id = ids[question]
                answer_type = all_questions[id]['answer_type']  # update
                if answer_type == 'rich_snip': # merging these two categories
                    answer_type = 'feat_snip'
                if answer_type == 'overview': # merging these two categories
                    answer_type = 'knowledge'
                if answer_type not in per_type_scores:
                    per_type_scores[answer_type] = []
                per_type_scores[answer_type].append(curr_score)
                if all_questions[id]['short_answer']:
                    per_type_scores['short_answer'].append(curr_score)
                else:
                    per_type_scores['long_answer'].append(curr_score)
            score += curr_score
        else:
            missing_examples.append(question)
    if ids:
        for t, list in per_type_scores.items():
            if len(list) > 1:
                avg_score = sum(list) / len(list)
                print(f" {t} \t {avg_score} \t {len(list)}")
    return (score / float(num_examples), num_examples, missing_examples)

def create_map(list1, list2):
    new_dict = {}
    for (key, value) in zip(list1, list2):
        if key in new_dict:
            new_dict[key].append(value)
        else:
            new_dict[key] = [value]
    return new_dict

if __name__ == "__main__":

    inputs = []
    targets = {}

    # parse command line arguments
    args = docopt(__doc__)
    eval_path = args["--eval_path"]
    eval_metric = args["--eval_metric"]
    if eval_path is not None:
        path_regex = r'gs://(?P<bucket_name>[^/]+)/(?P<file_path>.+)'
        m = re.match(path_regex, eval_path)
        bucket_name = m.groupdict()['bucket_name']
        path = m.groupdict()['file_path']
    else:
        model_mixture_name = args["--model_mixture_name"]
        dataset_mixture_name = args["--dataset_mixture_name"]
        bucket_name = args["--bucket_name"]
        model_size = args["--model_size"] if args["--model_size"] else "small"
        path = f't5-evaluations/model:{model_mixture_name}_eval:{dataset_mixture_name}/{model_size}/'

        input_sequence_length = args["--input_sequence_length"] if args['--input_sequence_length'] else 512
        output_sequence_length = args["--output_sequence_length"] if args['--output_sequence_length'] else 100
        sequence_length = {"inputs": input_sequence_length, "targets": output_sequence_length}

    print(f'Bucket name: {bucket_name}, Path: {path}')
    storage_client = storage.Client()
    blobs = list(storage_client.list_blobs(
        bucket_name, prefix=path
    ))


    def get_lines_from_file(bucket_name, file_name):
        full_file_name = f'gs://{bucket_name}/{file_name}'
        lines = []
        with tf.io.gfile.GFile(full_file_name) as ip_lines:
            for line in ip_lines:
                lines.append(line.strip())
        return lines

    inputs_file = ([blob for blob in blobs if blob.name.endswith('_inputs')])[0]
    inputs = get_lines_from_file(bucket_name, inputs_file.name)
    targets_file = ([blob for blob in blobs if blob.name.endswith('_targets')])[0]
    targets = get_lines_from_file(bucket_name, targets_file.name)
    targets = [target_line for target_line in targets]
    ids = None
    if "test_eval" in eval_path and 'short_answer' in eval_path and '_model:' not in eval_path:
        ids = [int(x.split("\t")[1]) for x in targets]
        ids = dict(zip(inputs, ids))
    targets = [x.split("\t")[0] for x in targets]
    targets = create_map(inputs, targets)

    num_targets = len(targets)
    if num_targets > 0:
        prediction_checkpoints = [blob for blob in blobs if blob.name.endswith('_predictions')]
        best_score = 0.0
        best_checkpoint = None
        best_checkpoint_num_examples = 0
        best_checkpoint_missing_examples = []
        best_checkpoint_predictions = []
        for prediction_checkpoint in prediction_checkpoints:
            if "1180400" not in prediction_checkpoint.name:
                print(f" Skipping: {prediction_checkpoint.name}")
                continue
            print(f'Evaluating prediction checkpoint {prediction_checkpoint.name}')
            predictions = get_lines_from_file(bucket_name, prediction_checkpoint.name)
            predictions = [x.split("\t")[0] for x in predictions]
            predictions = dict(zip(inputs, predictions))
            num_predictions = len(predictions)
            if num_predictions != num_targets:
                print('Something is wrong! The no. of predictions does not match no. of target labels.')
            score, num_examples, missing_examples = evaluate(targets, predictions, eval_metric, ids)
            print(f'Score on current checkpoint: {score}')
            if score > best_score:
                best_score = score
                best_checkpoint = prediction_checkpoint.name
                best_checkpoint_predictions = predictions
                best_checkpoint_num_examples = num_examples
                best_checkpoint_missing_examples = missing_examples
        print(
            f'Evaluated all checkpoints. Best checkpoint: {best_checkpoint}. Best score: {best_score} from {best_checkpoint_num_examples} questions. No. of missing questions: {len(best_checkpoint_missing_examples)}')
