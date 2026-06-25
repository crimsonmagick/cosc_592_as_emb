import gc
import logging

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer import modules

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def _get_model(model_name: str):
    if "starcoder" in model_name:
        word_embedding_model = modules.Transformer(
            model_name,
            max_seq_length=2048
        )
        if word_embedding_model.tokenizer.pad_token is None:
            word_embedding_model.tokenizer.pad_token = word_embedding_model.tokenizer.eos_token
        pooling_model = modules.Pooling(
            word_embedding_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True
        )

        return SentenceTransformer(modules=[word_embedding_model, pooling_model], device="cuda",
                                   model_kwargs={"torch_dtype": torch.bfloat16})
    return SentenceTransformer(model_name, device="cuda", model_kwargs={"torch_dtype": torch.bfloat16})

def generate_embeddings(model_name, disassemblies, *, batch_size):
    logger.info(f"BEGIN Generating embeddings for {model_name}")
    model = _get_model(model_name)
    embeddings = model.encode(disassemblies, batch_size=batch_size)
    logger.info(f"END Generating embeddings for {model_name}")
    del model
    gc.collect()
    torch.cuda.empty_cache()
    return embeddings