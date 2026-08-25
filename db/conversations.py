import uuid
from pymongo import ReturnDocument
from pymongo import DESCENDING
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from db.mongo import get_collection

# link of the docuemntation used: https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/index.html

# Mongo database consists of collections and each collection consists of documents
# In our project we will have a collection of conversations, so each conversation will represent a document.
# Each conversation is a document which has a title, unique id, date of last interaction, and dictionary of messages which represents the actual conversation.

conversations = get_collection("conversations")


def create_uid():
    return str(uuid.uuid4())

def get_time_now():
    return datetime.now(timezone.utc)

def create_new_conversation(title: str, role: str, content: str) -> str:
    unique_id = create_uid()
    last_interaction = get_time_now()
    doc = {
        "title" : title or "untitled conversation",
        "_id" : unique_id,
        "last_interaction" : last_interaction,
        "messages" : []
    }
    if role and content:
            doc["messages"].append({"role": role, "content": content, "ts": last_interaction})
    conversations.insert_one(doc)
    return unique_id

def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    last_interaction = get_time_now()
    doc = conversations.find_one_and_update(
        filter = {"_id":conv_id},
        update = {
            "$set": {"last_interaction": last_interaction}
        },
        return_document = ReturnDocument.AFTER
    )
    return doc
# db.collection.find_one_and_update(filter, update)
# find conversation, update it, and choose whether to return the original or the updated version.

def add_message(conv_id: str, role: str, content: str) -> bool:
    last_interaction = get_time_now()
    result = conversations.update_one(
        filter = {"_id": conv_id},
        update = {
            "$push" : {"messages": {"role": role, "content": content, "ts": last_interaction}},
            "$set" : {"last_interacted": last_interaction, "_id": conv_id}
        }
    )
    return (result.matched_count == 1)

# update_one(filter, update), update_many(filter, update) return an object that has 4 fields:
# matched_count, modified_count,  raw_server, and upserted_id.

def get_all_conversations() -> Dict[str, str]:
    result = conversations.find(
        filter = {},
        projection = {"title": 1}
    ).sort("last_interacted", DESCENDING) # Descending because during displaying, we want the most recent conversations at the top.
    return {doc["_id"]: doc["title"] for doc in result} # Dictionary comprehension

# this will be used to show the conversations at the left side panel, and that's why we erturned a dictionary of: "_id": "title", because we only care about the titles in the left side panel.

def delete_conversation(conv_id: str):
    conversations.delete_one(
        {"_id": conv_id}
    )

        
