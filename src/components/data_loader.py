
conversation=[]

def add_message_to_conversation(speaker,message):
    """adds message details to conversation \n
    speaker : str [user,consultant] \n
    message : str """
    conversation.append({"speaker": speaker,"text": message})

def get_full_conversation():
    """returns full conversation of a session"""
    return "\n".join([f"{msg['speaker'].capitalize()}: {msg['text']}" for msg in conversation])

def reset_conversation():
    """resets the conversation"""
    global conversation
    conversation=[]