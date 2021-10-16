import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model

def build_model(transformer, max_len=512):
    """
    https://www.kaggle.com/xhlulu/jigsaw-tpu-distilbert-with-huggingface-and-keras
    """
    input_word_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_ids")
    attention_mask = Input(shape=(max_len,), dtype=tf.int32, name="attention_mask")
    sequence_output = transformer(
        {"input_ids": input_word_ids, "attention_mask": attention_mask}
    )[0]
    cls_token = sequence_output[:, 0, :]
    out = Dense(1, activation="sigmoid")(cls_token)

    model = Model(
        inputs={"input_ids": input_word_ids, "attention_mask": attention_mask},
        outputs=out,
    )
    model.compile(Adam(lr=1e-5), loss="binary_crossentropy", metrics=["accuracy"])

    return model

