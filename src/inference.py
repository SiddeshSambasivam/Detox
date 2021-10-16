import pdb
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from transformers import TFAutoModel, AutoTokenizer

MAX_LEN = 192
MODEL = "joeddav/xlm-roberta-large-xnli"
# AUTO = tf.data.experimental.AUTOTUNE
# tokenizer = AutoTokenizer.from_pretrained(MODEL)
  
tokenizer = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")

# model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def dict_encode(texts, tokenizer, maxlen=512):
    enc_di = tokenizer.batch_encode_plus(
        texts,
        return_attention_mask=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        max_length=maxlen,
        truncation=True,
    )

    return {
        "input_ids": np.array(enc_di["input_ids"]),
        "attention_mask": np.array(enc_di["attention_mask"]),
    }


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


transformer_layer = TFAutoModel.from_pretrained(MODEL)
model = build_model(transformer_layer, max_len=MAX_LEN)

model.load_weights("./Checkpoints/detox_final_weights.h5")

sent_x = dict_encode(["你太棒了"], tokenizer, maxlen=MAX_LEN)
pdb.set_trace()

y = model(sent_x)
