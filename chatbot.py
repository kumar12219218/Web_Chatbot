from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.tools.tavily_search import TavilySearchResults

llm = ChatGroq(model="llama-3.1-8b-instant")
search_tool = TavilySearchResults(k=3)

def create_conversation_chain(query, past_history):
    memory = ConversationBufferMemory(return_messages=True)
    
    # Restore memory from past messages
    for item in past_history:
        memory.chat_memory.add_user_message(item["user"])
        memory.chat_memory.add_ai_message(item["bot"])

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

    # Search the web and add it to context
    search_results = search_tool.invoke({"query": query})
    web_context = "\n".join([r["content"] for r in search_results])
    augmented_query = f"{query}\n\nHere are some current search results:\n{web_context}"

    response = conversation.predict(input=augmented_query)

    # Update memory for session
    past_history.append({"user": query, "bot": response})
    return response, past_history
