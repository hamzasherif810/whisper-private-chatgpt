from llama_index.core.llms import ChatMessage, MessageRole
from llm_factory.get_llm import get_llm
from typing import Dict, Any


def get_answer(model_name: str, chat_history: list[Dict[str, Any]]) -> str:
    llm = get_llm(model_name)
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful chat assistant.")
    ]

    messages.extend(
        [ChatMessage(role=message["role"], content=message["content"]) for message in chat_history]
    )

    response = llm.chat(messages=messages)
    return response.message.content

# So in our project, any conversation is doc that have many fields like the last_interaction, the title, and the messages dictionary.
# In order for the model to understand the whole context of the conversation, every time you talk to him, you must send him all the previous messages in the conversation.
# To do that, we implemented the get_answer function that takes the chat_history. To get the chat_history we will use the get_conversation function to return the dictionary of messages for this specific conversation.
