

# import ollama
# response = ollama.chat(
#     model='llama3',
#     stream=True,
#     messages=[
#     {
#      'role': 'system',
#      'content': 'You are a child who loves science',
#     },
#     {
#     'role': 'user',',
#     },
# ])

#     'content': 'Why is the sky blue?
# for chunk in response:
#   print(chunk['message']['content'], end='', flush=True)
#   print()




# Importing the required library (ollama)
import ollama
model="llama3"
# Initializing an empty list for storing the chat messages and setting up the initial system message
system_message='You are a helpful assistant.'
chat_messages = [{"role":"system","content":system_message}]

# Defining a function to create new messages with specified roles ('user' or 'assistant')
def create_message(message, role):
  return {
    'role': role,
    'content': message
  }

# Starting the main conversation loop
def chat():
  # Calling the ollama API to get the assistant response
    ollama_response = ollama.chat(model=model, stream=True, messages=chat_messages)

  # Preparing the assistant message by concatenating all received chunks from the API
    assistant_message = ''
    for chunk in ollama_response:
        assistant_message += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    print("\n")

  # Adding the finalized assistant message to the chat log
    chat_messages.append(create_message(assistant_message, 'assistant'))

# Function for asking questions - appending user messages to the chat logs before starting the `chat()` function
def ask(message):
    chat_messages.append(
        create_message(message, 'user')
    )
    chat()

# Sending two example requests using the defined `ask()` function
while True:
    user_input=input(">>>>>  ")
    if user_input=="model":
        model=input("Ollama model:  ")
        print()
    elif user_input=="prompt":
        chat_messages[0]["content"]=input("System prompt:  ")
        print()
    elif user_input=="/bye":
        break
    else:
        ask(user_input)
        # for i in chat_messages:
        #     print(i)
