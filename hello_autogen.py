from autogen import ConversableAgent, config_list_from_json


config_list = config_list_from_json("config_list_local.json")
llm_config = {"config_list": config_list}

class SimpleAssistant(ConversableAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

class SimpleUser(ConversableAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, human_input_mode="NEVER", llm_config=llm_config)


assistant = SimpleAssistant(name="assistant", llm_config=llm_config)
user = SimpleUser(name="user", llm_config=llm_config)


user.initiate_chat(assistant, message="Can you say hello?")
