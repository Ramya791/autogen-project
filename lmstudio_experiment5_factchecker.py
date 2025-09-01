from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json


config_list = config_list_from_json("config_list_local.json")


user = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    system_message="You ask factual questions.",
    code_execution_config={"use_docker": False}
)


retriever = AssistantAgent(
    name="retriever",
    system_message=(
       "You are a retrieval assistant. Produce 2–3 concise bullets prefixed 'Evidence:'. "
        "If unsure about a fact, write 'Unknown'. Do NOT answer the question."

    ),
    llm_config={"config_list": config_list}
)


verifier = AssistantAgent(
    name="verifier",
    system_message=(
        "You are a verifier. Check the evidence for contradictions or obvious factual errors. "
        "If any item looks wrong, say 'Correction:' and fix it, then provide a one-sentence final answer. "
        "End with TERMINATE."
    ),
    llm_config={"config_list": config_list}
)


groupchat = GroupChat(
    agents=[user, retriever, verifier],
    messages=[],
    max_round=6,
    speaker_selection_method="round_robin"
)


manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list},
    is_termination_msg=lambda m: isinstance(m.get("content"), str) and "TERMINATE" in m["content"]
)


question = "Who was Ada Lovelace and why is she significant in computing history?"
user.initiate_chat(manager, message=question)


# o/p
# (venv) C:\Users\sri79\autogen-project>python application2.py
# user (to chat_manager):

# Who was Ada Lovelace and why is she significant in computing history?

# --------------------------------------------------------------------------------

# Next speaker: retriever

# [autogen.oai.client: 08-21 18:32:21] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# retriever (to chat_manager):


# Evidence:
# 1. Ada Lovelace was an English mathematician who lived during the Victorian era. She was born into a family of scientists, and her father, Charles Babbage, is considered to be the father of modern computing.
# 2. Ada Lovelace is significant in computing history for several reasons. One of these is that she is credited with being the world's first computer programmer, having written code for her father's Analytical Engine in the mid-19th century.
# 3. Another reason why Ada Lovelace is important is that she recognized the potential of computers to perform more than just mechanical calculations. In a paper she wrote in 1852, she predicted that computers would one day be capable of playing games and composing music. This visionary thinking has helped shape the future of computing and its many applications.

# --------------------------------------------------------------------------------

# Next speaker: verifier

# [autogen.oai.client: 08-21 18:34:00] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# verifier (to chat_manager):

# Ada Lovelace was an English mathematician who is significant in computing history for being the world's first computer programmer and recognizing the potential of computers to perform more than just mechanical calculations.

# TERMINATE.

# --------------------------------------------------------------------------------

# >>>>>>>> TERMINATING RUN (31afd8b2-4c43-4611-9ec5-f60da78e01a3): Termination message condition on the GroupChatManager 'chat_manager' met

# (venv) C:\Users\sri79\autogen-project>