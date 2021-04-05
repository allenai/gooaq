########################## Qoogle: google_answers_short_answers #################################
export TPU_NAME=...
export PROJECT=...
export ZONE=...
export BUCKET=...

PRETRAINED_STEPS=1000000
FINETUNE_STEPS=20000
declare -a sizes=("11B" "small")
declare -a tasks=("google_answers_short_answers_v6_size_2000" "google_answers_short_answers_v6_size_20000" "google_answers_short_answers_v6_size_200000")

for SIZE in "${sizes[@]}"; do
  for TASK in "${tasks[@]}"; do

  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

    # Run fine-tuning
    python -m t5.models.mesh_transformer_main \
      --module_import="qoogle_tasks" \
      --tpu="${TPU_NAME}" \
      --gcp_project="${PROJECT}" \
      --tpu_zone="${ZONE}" \
      --model_dir="${MODEL_DIR}" \
      --gin_file="dataset.gin" \
      --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
      --gin_param="utils.run.save_checkpoints_steps=1000" \
      --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
      --gin_param="MIXTURE_NAME = '${TASK}'" \
      --gin_param="utils.run.batch_size=('tokens_per_batch', 196608)" \
      --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
      --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
      --t5_tfds_data_dir="${BUCKET}/t5-tfds"

    # Run eval
    python -m t5.models.mesh_transformer_main \
      --module_import="qoogle_tasks" \
      --tpu="${TPU_NAME}" \
      --gcp_project="${PROJECT}" \
      --tpu_zone="${ZONE}" \
      --model_dir="${MODEL_DIR}" \
      --gin_file="dataset.gin" \
      --gin_file="${MODEL_DIR}/operative_config.gin" \
      --gin_file="eval.gin" \
      --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
      --gin_param="MIXTURE_NAME = '${TASK}'" \
      --gin_param="utils.run.dataset_split = 'dev'" \
      --gin_param="utils.run.eval_checkpoint_step='all'" \
      --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done


########################## Qoogle: google_answers_long_answers #################################
PRETRAINED_STEPS=1000000
FINETUNE_STEPS=2000000

declare -a sizes=("11B" "small")
declare -a tasks=("google_answers_long_answers_v6_size_2000" "google_answers_long_answers_v6_size_20000" "google_answers_long_answers_v6_size_2000000")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run fine-tuning
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
    --gin_param="utils.run.save_checkpoints_steps=1000" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 196608)" \
    --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
    --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  # Run eval
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.run.eval_checkpoint_step=1004400" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.run.eval_checkpoint_step=1004400" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done

########################## Qoogle: google_answers_long_answers #################################
PRETRAINED_STEPS=1000000
FINETUNE_STEPS=20000

declare -a sizes=("11B" "small")
declare -a tasks=("google_answers_long_answers_v6_size_200000" "google_answers_long_answers_v6_size_2000000")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run fine-tuning
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
    --gin_param="utils.run.save_checkpoints_steps=1000" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 196608)" \
    --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
    --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  # Run eval
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done


########################## Qoogle: google_answers_collection_answers #################################
PRETRAINED_STEPS=1000000
FINETUNE_STEPS=20000

declare -a sizes=("11B" "small")
declare -a tasks=("google_answers_collection_answers_v6_size_2000" "google_answers_collection_answers_v6_size_20000" "google_answers_collection_answers_v6_size_200000")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"

  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run fine-tuning
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
    --gin_param="utils.run.save_checkpoints_steps=1000" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 196608)" \
    --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
    --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  # Run eval
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-128'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done

######### evaluate our models on eli5
declare -a sizes=("small" "11B")
declare -a tasks=("google_answers_long_answers_v6_size_200000" "google_answers_long_answers_v6_size_20000" "google_answers_long_answers_v6_size_2000" "google_answers_long_answers_v6_size_2000000")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run eval on eli5
  TASK=eli5
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done

######### train t5 on eli5
PRETRAINED_STEPS=1000000
FINETUNE_STEPS=200000

declare -a sizes=("small" "11B")
declare -a tasks=("eli5")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run fine-tuning
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
    --gin_param="utils.run.save_checkpoints_steps=5000" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
    --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  # Run eval
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done


######### train t5 on eli5 + Qoogle
PRETRAINED_STEPS=1000000
FINETUNE_STEPS=200000

declare -a sizes=("small" "11B")
declare -a tasks=("eli5_w_google_answers_long_answers")

for TASK in "${tasks[@]}"; do
for SIZE in "${sizes[@]}"; do
  PRETRAINED_DIR="gs://t5-data/pretrained_models/${SIZE}"
  MODEL_DIR="${BUCKET}/${TASK}/${SIZE}"

  # Run fine-tuning
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${PRETRAINED_DIR}/operative_config.gin" \
    --gin_param="utils.run.save_checkpoints_steps=5000" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.train_steps=$((PRETRAINED_STEPS + FINETUNE_STEPS))" \
    --gin_param="utils.run.init_checkpoint='${PRETRAINED_DIR}/model.ckpt-${PRETRAINED_STEPS}'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  # Run eval
  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'dev'" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"

  python -m t5.models.mesh_transformer_main \
    --module_import="qoogle_tasks" \
    --tpu="${TPU_NAME}" \
    --gcp_project="${PROJECT}" \
    --tpu_zone="${ZONE}" \
    --model_dir="${MODEL_DIR}" \
    --gin_file="dataset.gin" \
    --gin_file="${MODEL_DIR}/operative_config.gin" \
    --gin_file="eval.gin" \
    --gin_param="utils.tpu_mesh_shape.tpu_topology = 'v3-8'" \
    --gin_param="MIXTURE_NAME = '${TASK}'" \
    --gin_param="utils.run.dataset_split = 'test'" \
    --gin_param="utils.tpu_mesh_shape.model_parallelism = 8" \
    --gin_param="utils.run.batch_size=('tokens_per_batch', 4096)" \
    --gin_param="utils.run.eval_checkpoint_step='all'" \
    --t5_tfds_data_dir="${BUCKET}/t5-tfds"
done
done