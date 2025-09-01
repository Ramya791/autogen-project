from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


config_list = config_list_from_json("config_list_local.json")


llm_config = {
    "config_list": config_list,
    "temperature": 0.0,
    "max_tokens": 96
}

SYSTEM_MSG = (
    "You are a precise conversational calculator.\n"
    "Rules:\n"
    "1) For EVERY math request, write a minimal Python code block that computes the answer.\n"
    "2) Always print the final result as: Output: <number or value>\n"
    "3) Do not add explanations unless the user asks.\n"
    "4) Support follow-ups that reference the previous result when the user says 'now', 'then', etc.\n"
    "5) If the request is unclear, ask a short clarifying question."
)

assistant = AssistantAgent("calc_assistant", llm_config=llm_config, system_message=SYSTEM_MSG)


user = UserProxyAgent(
    "user",
    code_execution_config={"use_docker": False, "work_dir": "./"},
    human_input_mode="ALWAYS"
)

print("\nConversational Calculator. Type 'exit' to finish.\n")
user.initiate_chat(
    assistant,
    message="Hi! I will ask you math questions in plain English. Wait for my inputs.",
    max_turns=20,  
)



# output:

# (venv) C:\Users\sri79\autogen-project>python lmstudio_experiment1_calculator.py

# Conversational Calculator. Type 'exit' to finish.

# user (to calc_assistant):

# Hi! I will ask you math questions in plain English. Wait for my inputs.

# --------------------------------------------------------------------------------
# [autogen.oai.client: 08-23 16:15:09] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# calc_assistant (to user):

# Hello! I'm ready to help with your math questions. Please go ahead and ask your first question.

# --------------------------------------------------------------------------------
# Replying as user. Provide feedback to calc_assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: how much is 23 + 50
# user (to calc_assistant):

# how much is 23 + 50

# --------------------------------------------------------------------------------
# [autogen.oai.client: 08-23 16:15:53] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# calc_assistant (to user):

# Output: 73

# --------------------------------------------------------------------------------
# Replying as user. Provide feedback to calc_assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: can you tell me what is 24 divided by 2
# user (to calc_assistant):

# can you tell me what is 24 divided by 2

# --------------------------------------------------------------------------------
# [autogen.oai.client: 08-23 16:17:41] {696} WARNING - Model mistral-7b-instruct-v0.1 is not found. The cost will be 0. In your config_list, add field {"price" : [prompt_price_per_1k, completion_token_price_per_1k]} for customized pricing.
# calc_assistant (to user):

# Output: 12



# --------------------------------------------------------------------------------
# Replying as user. Provide feedback to calc_assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: exit

# >>>>>>>> TERMINATING RUN (d567dddd-3e05-4d93-9332-5655317554ab): User requested to end the conversation