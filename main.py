import streamlit as st


from services.get_models_list import get_models
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
    delete_conversation
)

st.set_page_config(page_title="Private ChatGPT", page_icon="💬")
st.title("🤫 WhisperGPT")

if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_models()

# st.session_state is a dictionary-like object — Streamlit's "backpack" that survives reruns within the same browser session.
# Every subsequent rerun (button clicks, sending messages, etc.): the backpack already has "OLLAMA_MODELS", so this condition is False. It just reuses what's already stored.
selected_model = st.selectbox("Select Model", st.session_state.OLLAMA_MODELS)


st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])  # [{role, content}]


# .setdefault(key, default) is a standard Python dict method: "if this key doesn't exist yet, create it with this default value.
# If it already exists, do nothing — leave it alone."

# This is functionally the same idea as the if "X" not in st.session_state: pattern above, just written more compactly for three keys at once.
# It's safe to run on every single rerun because it never overwrites existing values — it only fills in gaps the first time.

# these three variables are important to know after reruns which conversation is active and displays its title and its messages
# so they control the real body of the chat 

with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()  # {conv_id: title, .....}

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []
    # st.button(label) draws a button and returns True only on the one rerun immediately triggered by clicking it — on every other rerun, it returns False.
    # The reason why we reseted the conv_id, conv_title, and the chat_history is because the new chat doesn't have any of them until at least one message is sent.
    
    for cid, title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title # this bolds only the active conversation

        col1, col2 = st.columns([0.9, 0.1])

        with col1:
            if st.button(label, key=f"conv_{cid}"): # returns True only on the one rerun immediately triggered by clicking it
                doc = get_conversation(cid) or {} # remember get_conversation(id) returns a conversation document with that specific id. 
                st.session_state.conversation_id = cid
                st.session_state.conversation_title = doc.get("title", "Untitled")
                st.session_state.chat_history = [
                    {"role": m["role"], "content": m["content"]} for m in doc.get("messages", [])
                ]

        with col2:
            if st.button("x", key=f"del_{cid}"):
                delete_conversation(cid)  # your DB delete function
                # If the deleted conversation is the one currently open, reset to new chat
                if st.session_state.conversation_id == cid:
                    st.session_state.conversation_id = None
                    st.session_state.conversation_title = None
                    st.session_state.chat_history = []

                st.rerun()
    # This for loop loops over the conversations and display them at the left side panel as buttons with their titles and only the active conversation title is bolded
    # It also do an if condition for the pressed button and then configure the conversation_id, conversation_title, and chat_history.

# After setting up all the variables, now its time to physically show the messages of the active conversation.
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_query = st.chat_input("Ask AI...")
if user_query:
    # 1) show + store the message in UI state
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role":"user", "content":user_query})

    #2) persist to database (create conversation on first message, else append)
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model, user_query)
        except Exception as e:
            title = f"Error: {e}"
        conv_id = create_new_conversation(title, role="user", content=user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_message(st.session_state.conversation_id, "user", user_query) # remember this function appends a new message in the current conversation with role, content, and ts

    #3) Get assistance response
    try:
        assistant_text = get_answer(selected_model, st.session_state.chat_history)
    except Exception as e:
        assistant_text = f"Error getting response: {e}"

    #4) show + store assistant message
    st.chat_message("assistant").markdown(assistant_text)
    st.session_state.chat_history.append({"role":"assistant", "content":assistant_text})
    # 5) Persist assistant message
    add_message(st.session_state.conversation_id, "assistant", assistant_text)