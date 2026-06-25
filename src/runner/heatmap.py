from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity


def generate_heatmaps(embeddings, *, model_name, function_names, group_size, out_dir):
    similarities = cosine_similarity(embeddings)
    embedding_dim = embeddings.shape[1]
    plt.figure(figsize=(12, 10))

    dis_hm = sns.heatmap(
        similarities,
        cmap="magma",
        xticklabels=False,
        yticklabels=False,
        square=True
    )

    for i in range(0, len(similarities) + 1, group_size):
        dis_hm.axhline(i, color="white", linewidth=2)
        dis_hm.axvline(i, color="white", linewidth=2)

    centers = [i * 9 + 4 for i in range(len(function_names))]

    dis_hm.set_xticks(centers)
    dis_hm.set_yticks(centers)

    dis_hm.set_xticklabels(function_names, rotation=45, ha="right")
    dis_hm.set_yticklabels(function_names)

    plt.title(f"{model_name} (embedding_dim={embedding_dim})")
    plt.tight_layout()
    plt.savefig(Path(out_dir, f"{model_name.replace('/', '_')}_heatmap.png"))
