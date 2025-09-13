This repository contains experiments from my MSc dissertation : Investigating Autogen

#Setup instructions
- clone the repo :   _ git clone https://github.com/<your-username>/autogen-project.git_
- create and activate virtual environment
  _ python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows_
- install dependencies 
- Start lm studio with an open ai compatible server. Select Mistral-7B-Instruct and enable server at http://127.0.0.1:1234/v1.
- Update config_list_local.json to point to the correct LM Studio endpoint


#Running experiments
- Experiment 1 - Calculator agent: Structured prompting and function like execution
- Experiment 2 - Simple Chat : Role based turn taking with moderation
- Experiment 3 - Fact Finder : Retrieval Augmented Generation with local corpus
- Experiment 4 - PII Redaction : Privacy preserving text redaction with multi agent review
- Experiment 5 - Fact checker : Multi-step retrieval and verification


#Execute any experiment when in the virtual env : python lmstudio_experiment1_calculator.py
