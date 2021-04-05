import random
import t5
import os
import functools
import tensorflow as tf
from t5.data import sentencepiece_vocabulary
from t5.evaluation import metrics

DATA_DIR = "gs://danielk-files/data/"


def get_downloaded_data_path(data_dir1, split, extension):
    return os.path.join(data_dir1, split + extension)


def preprocess(
        dataset,
        prefix='',  # not used
        sample_answer=False,  # not used
):
    return dataset.filter(lambda ex: tf.strings.length(ex['targets']) > 0)


def dataset_fn(split, shuffle_files=False, dataset=""):
    # Load lines from the text file as examples.
    ds = tf.data.TextLineDataset(get_downloaded_data_path(DATA_DIR + dataset, split, ".tsv"))
    print(" >>>> about to read tsv . . . ")
    ds = ds.map(
        functools.partial(tf.io.decode_csv, record_defaults=["", "", ""], use_quote_delim=False, field_delim="\t"),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # Map each tuple to a {"question": ... "answers": ...} dict.
    ds = ds.map(lambda *ex: dict(zip(["inputs", "targets", "id"], ex)))
    return ds


def dataset_fn_two_column(split, shuffle_files=False, dataset=""):
    # Load lines from the text file as examples.
    ds = tf.data.TextLineDataset(get_downloaded_data_path(DATA_DIR + dataset, split, ".tsv"))
    print(" >>>> about to read tsv . . . ")
    ds = ds.map(
        functools.partial(tf.io.decode_csv, record_defaults=["", ""], use_quote_delim=False, field_delim="\t"),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # Map each tuple to a {"question": ... "answers": ...} dict.
    ds = ds.map(lambda *ex: dict(zip(["inputs", "targets"], ex)))
    return ds


def postprocessor(answer, example=None, is_target=False):
    """Returns answer, or all answers if the full example is provided."""
    if example:
        return tf.compat.as_text(answer) + "\t" + tf.compat.as_text(example["id"])
    else:
        return answer


def postprocessor_two_column(answer, example=None, is_target=False):
    """Returns answer, or all answers if the full example is provided."""
    return tf.compat.as_text(answer)


for task in [
    'google_answers_collection_answers_v6_size_20000',
    'google_answers_collection_answers_v6_size_200000',
    'google_answers_collection_answers_v6_size_2000',
    'google_answers_long_answers_v6_size_200000',
    'google_answers_long_answers_v6_size_2000000',
    'google_answers_long_answers_v6_size_2000',
    'google_answers_long_answers_v6_size_20000',
    'google_answers_short_answers_v6_size_2000',
    'google_answers_short_answers_v6_size_20000',
    'google_answers_short_answers_v6_size_200000'
]:
    t5.data.TaskRegistry.add(
        task,
        # Supply a function which returns a tf.data.Dataset.
        dataset_fn=functools.partial(dataset_fn, dataset=task),
        splits=["train", "test", "dev"],
        # Supply a function which preprocesses text from the tf.data.Dataset.
        text_preprocessor=preprocess,
        # Lowercase targets before computing metrics.
        postprocess_fn=postprocessor,
        # sentencepiece_model_path=t5.data.DEFAULT_SPM_PATH,
        metric_fns=[metrics.squad]
    )

for task in [
    'natural_questions_direct_ans',
    'webquestions',
    'triviaqa_direct_ans',
    'natural_questions_with_dpr_para',
    'squad1_1',
    'squad2',
    'newsqa',
    'ropes_test',
    'quoref',
    'narrativeqa',
    'summarization_xsum_dev',
    'eli5'
]:
    t5.data.TaskRegistry.add(
        task,
        # Supply a function which returns a tf.data.Dataset.
        dataset_fn=functools.partial(dataset_fn_two_column, dataset=task),
        splits=["train", "test", "dev"],
        # Supply a function which preprocesses text from the tf.data.Dataset.
        text_preprocessor=preprocess,
        # Lowercase targets before computing metrics.
        postprocess_fn=postprocessor_two_column,
        # sentencepiece_model_path=t5.data.DEFAULT_SPM_PATH,
        metric_fns=[metrics.squad]
    )

# for task in [
#     'natural_questions_direct_ans',
#     'webquestions',
#     'triviaqa_direct_ans',
# ]:
#     t5.data.MixtureRegistry.add(
#         f"{task}_w_google_answers_short_answers",
#         [task, "google_answers_short_answers_v5"],
#         default_rate=1.0)

t5.data.MixtureRegistry.add(
    f"eli5_w_google_answers_long_answers",
    ['eli5', "google_answers_long_answers_v6_size_2000000"],
    default_rate=1.0
)