# import os
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain



# # 0️⃣ Set your OpenAI API key here

# os.environ["OPENAI_API_KEY"] = "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"  # Replace with your real key



# # 1️⃣ Initialize the OpenAI LLM

# llm = OpenAI(model_name="gpt-4o", temperature=0.2)



# # 2️⃣ Wrap your prompt

# prompt = PromptTemplate(

#     input_variables=["topic"],

#     template="Explain the following topic in simple terms: {topic}"

# )



# # 3️⃣ Create the LLMChain

# chain = LLMChain(llm=llm, prompt=prompt)



# # 4️⃣ Run the chain with your input

# response = chain.run("Quantum Entanglement")

# print(response)

# ✅ 1. Use the new community imports
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# ✅ 2. Define your prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Tell me about {topic}.")
])

# ✅ 3. Set up the LLM
# llm = ChatOpenAI(
#     model="gpt-4o",
# )
llm = ChatOpenAI(openai_api_key="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", model="gpt-4o")


# ✅ 4. Create a runnable chain
chain = prompt | llm

# ✅ 5. Run the chain with invoke() instead of run()
response = chain.invoke({"topic": "Quantum Entanglement"})
print(response.content)
