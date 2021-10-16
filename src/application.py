import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from transformers import TFAutoModel, AutoTokenizer

from model import build_model
from tokenizer import dict_encode

# FLASK Configs
app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

PORT = int(os.environ.get("PORT", 10000))

MAX_LEN = 192
MODEL = "joeddav/xlm-roberta-large-xnli"
tokenizer = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")

transformer_layer = TFAutoModel.from_pretrained(MODEL)
model = build_model(transformer_layer, max_len=MAX_LEN)

model.load_weights("./Checkpoints/detox_final_weights.h5")


@app.route("/api", methods=["GET"])
def endpoint():
    query = dict()
    params = request.args.to_dict()  # parse user params

    # Single query "
    text = params["sent"]
    tkn_text = dict_encode([text], tokenizer, maxlen=MAX_LEN)
    
    y = model(tkn_text)

    response = {
        "sentence":text,
        "profanity":float(y.numpy()[0][0])
    }

    return jsonify(response)

app.run(host="0.0.0.0", port=PORT)
