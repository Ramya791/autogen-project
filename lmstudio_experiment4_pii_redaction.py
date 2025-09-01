from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json

config_list = config_list_from_json("config_list_local.json")

user = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    system_message="You provide text to be processed.",
    code_execution_config={"use_docker": False}
)

redactor = AssistantAgent(
    name="redactor",
    system_message="You are a PII redaction assistant. "
                   "Your job is to replace names, emails, phone numbers, and locations with [REDACTED].",
    llm_config={"config_list": config_list}
)

reviewer = AssistantAgent(
    name="reviewer",
    system_message="You are a reviewer. Check if the text is properly redacted. "
                   "If anything is missed, point it out.",
    llm_config={"config_list": config_list}
)


groupchat = GroupChat(
    agents=[user, redactor, reviewer],
    messages=[],
    max_round=3,
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}  
)

input_text = "My name is Alice, my email is alice123@gmail.com, and I live in Dublin."
user.initiate_chat(manager, message=f"Please redact the following text: {input_text}")





# o/p :

# (venv) C:\Users\sri79\autogen-project>python application1.py
# user (to chat_manager):

# Please redact the following text: My name is Alice, my email is alice123@gmail.com, and I live in Dublin.

# --------------------------------------------------------------------------------
# [autogen.oai.client: 08-21 17:50:34] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.

# Next speaker: redactor

# [autogen.oai.client: 08-21 17:52:09] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# redactor (to chat_manager):

# My name is [REDACTED], my email is [REDACTED], and I live in [REDACTED].

# --------------------------------------------------------------------------------
