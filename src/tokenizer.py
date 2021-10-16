import numpy as np

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
