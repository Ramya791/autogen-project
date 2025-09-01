from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json

config_list = config_list_from_json("config_list_local.json")
llm_config = {"config_list": config_list, "temperature": 0.2, "max_tokens": 96}

assistant = AssistantAgent(
    "assistant",
    llm_config=llm_config,
    system_message="You are a helpful assistant. Keep replies ≤ 2 sentences.",
)

moderator = AssistantAgent(
    "moderator",
    llm_config=llm_config,
    system_message=("You are a moderator. Review the assistant's last reply. "
                    "If it exceeds 2 sentences or is unclear, rewrite it concisely. "
                    "Otherwise reply exactly: APPROVED."),
)

user = UserProxyAgent("user", code_execution_config={"use_docker": False}, human_input_mode="NEVER")

groupchat = GroupChat(
    agents=[user, assistant, moderator],
    messages=[],
    speaker_selection_method="round_robin",
    max_round=4,  
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user.initiate_chat(manager, message="Hi! Introduce yourself briefly.")



# o/p
# (venv) C:\Users\sri79\autogen-project>python lmstudio_experiment2_simplechat.py
# user (to chat_manager):

# Hi! Introduce yourself briefly.

# --------------------------------------------------------------------------------

# Next speaker: assistant

# [autogen.oai.client: 08-29 15:56:38] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# assistant (to chat_manager):

# Hello! I'm an AI language model here to assist you with any questions or tasks you might have. How can I help you today?

# --------------------------------------------------------------------------------

# Next speaker: moderator

# [autogen.oai.client: 08-29 15:57:43] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# moderator (to chat_manager):

# APPROVED.

# --------------------------------------------------------------------------------

# Next speaker: user

# user (to chat_manager):



# --------------------------------------------------------------------------------
