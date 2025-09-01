import os, math
from typing import List, Tuple
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from openai import OpenAI

BASE_URL = "http://127.0.0.1:1234/v1"  
EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"
CORPUS_DIR = "./corpus"

def read_corpus() -> List[Tuple[str,str]]:
    docs = []
    for fn in os.listdir(CORPUS_DIR):
        if fn.lower().endswith(".txt"):
            path = os.path.join(CORPUS_DIR, fn)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            size = 800
            for i in range(0, len(text), size):
                chunk = text[i:i+size].strip()
                if chunk:
                    docs.append((f"{fn}#chunk{i//size}", chunk))
    return docs

def embed(texts: List[str]) -> List[List[float]]:
    client = OpenAI(base_url=BASE_URL, api_key="lm-studio")
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(sum(x*x for x in a)) + 1e-9
def cosine(a,b): return dot(a,b)/(norm(a)*norm(b))

print("Indexing corpus...")
docs = read_corpus()
ids  = [d[0] for d in docs]
txts = [d[1] for d in docs]
vecs = embed(txts)
print(f"Indexed {len(docs)} chunks from {len(set(i.split('#')[0] for i in ids))} files.")

def retrieve(q: str, k=3):
    qv = embed([q])[0]
    sims = [(cosine(qv, v), i) for i, v in enumerate(vecs)]
    sims.sort(reverse=True)
    top = sims[:k]
    return [(ids[i], txts[i]) for _, i in top]

config_list = config_list_from_json("config_list_local.json")
llm_cfg = {"config_list": config_list, "temperature": 0.1, "max_tokens": 220}

answerer = AssistantAgent(
    "answerer",
    llm_config=llm_cfg,
    system_message=(
        "Answer ONLY using the provided context snippets. "
        "If the answer is not present, say: INSUFFICIENT CONTEXT. "
        "Cite the snippet IDs you used like [file.txt#chunk0]."
    ),
)
user = UserProxyAgent("user", code_execution_config={"use_docker": False}, human_input_mode="NEVER", default_auto_reply="TERMINATE")

def ask(question: str):
    ctx = retrieve(question, k=3)
    ctx_block = "\n\n".join([f"[{cid}]\n{t}" for cid, t in ctx])
    prompt = (f"Question: {question}\n\n"
              f"Context snippets (use strictly):\n{ctx_block}\n\n"
              "Answer in 2–3 sentences and include the snippet IDs you used.")
    user.initiate_chat(answerer, message=prompt)

if __name__ == "__main__":
    print("\nRAG Fact Finder ready.")
    ask("Tell me something about Maynooth University in Ireland?")





# (venv) C:\Users\sri79\autogen-project>python fact_finder.py
# Indexing corpus...
# Indexed 3 chunks from 3 files.

# RAG Fact Finder ready.
# user (to answerer):

# Question: Who was Ada Lovelace and what did she contribute?

# Context snippets (use strictly):
# [ada.txt#chunk0]
# Ada Lovelace was a 19th-century mathematician and writer who is often regarded as the first computer programmer. She is known for her work on Charles Babbage's early mechanical general-purpose computer, the Analytical Engine. Lovelace was the first to recognize that the machine had applications beyond pure calculation, and she published the first algorithm intended to be carried out by such a machine.

# [autogen.txt#chunk0]
# AutoGen is a multi-agent orchestration framework developed by Microsoft for building applications powered by large language models. It enables developers to define multiple agents with specific roles and facilitates structured, turn-based communication between them. AutoGen supports integration with both cloud-based APIs and local models using OpenAI-compatible endpoints.

# [mistral.txt#chunk0]
# Mistral 7B is a state-of-the-art open-weight language model developed by Mistral AI. It is known for its efficiency and strong performance on a wide range of natural language processing tasks. The model is available in multiple formats, including GGUF, which is optimized for CPU and GPU inference through libraries like llama.cpp.

# Answer in 2–3 sentences and include the snippet IDs you used.


# (venv) C:\Users\sri79\autogen-project>python lmstudio_experiment3_factfinder.py
# Indexing corpus...
# Indexed 3 chunks from 3 files.

# RAG Fact Finder ready.
# user (to answerer):

# Question: Tell me something about Maynooth University in Ireland?

# Context snippets (use strictly):
# [mu.txt#chunk0]
# Maynooth University, is a constituent university of the National University of Ireland in Maynooth, County Kildare, Ireland. Maynooth University was formerly known as National University of Ireland,

# [mistral.txt#chunk0]
# Mistral 7B is a state-of-the-art open-weight language model developed by Mistral AI. It is known for its efficiency and strong performance on a wide range of natural language processing tasks. The model is available in multiple formats, including GGUF, which is optimized for CPU and GPU inference through libraries like llama.cpp.

# [autogen.txt#chunk0]
# AutoGen is a multi-agent orchestration framework developed by Microsoft for building applications powered by large language models. It enables developers to define multiple agents with specific roles and facilitates structured, turn-based communication between them. AutoGen supports integration with both cloud-based APIs and local models using OpenAI-compatible endpoints.

# Answer in 2–3 sentences and include the snippet IDs you used.

# --------------------------------------------------------------------------------
# [autogen.oai.client: 08-31 16:28:19] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# answerer (to user):

# Maynooth University is a constituent university of the National University of Ireland located in Maynooth, County Kildare, Ireland [mu.txt#chunk0]. It was formerly known as National University of Ireland.

