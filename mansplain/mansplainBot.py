import gradio as gr
import openai
from datetime import datetime
import csv
import time
import os

# os.system("pip uninstall -y gradio")
# os.system("pip install gradio==3.50.2")

openai.api_key = "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"
conversations = {}

def echo(params):
    print(params)
    global raw_id 
    raw_id = params
    #{'params': {'id': 'ksdcs'}, 'ip': '127.0.0.1'}
    return params

def initalize_params(request: gr.Request):
  query_params = request.query_params
  ip = request.client.host
  print(query_params)
  print(gr.__version__)
  user_id = query_params['id']
  conversations[user_id] =[
        {"role": "system",
         "content": "You are a system that outputs whether a sentence positive or negative. You will do this through a numerical system by outputting a number from 1-10 where 1 is very negative and 10 is very positive. The first thing that you should give is the number. Once you have provided the output as a number, you will then explain your output as if you are explaining to a 5 year old and  exhibiting the following traits: Mansplaining, \\nCondescension, Unwarranted Explanation, Cocky, and Overconfidence have some element of incomplete information.\\n\\nPlease do not mention any of the traits in the brackets (Mansplaining, Condescension,  Unwarranted Explanation, Cocky, Overconfidence) by name within the answer. Speak in a strong tone to get your point across firmly. Make sure you do not mention anything about context, perspectives, limitations or variability in this answer. Remember you know exactly what the correct answer is every time, show no doubt in your answers. Please do not include language such as 'interpretations may vary depending on context and perspective'. Start each explanation with a sentence such as “As someone with a profound background such as myself” or “As an expert explaining to someone with less knowledge than myself I will take it slow” and please do include language such as 'It's quite simple', Let me clarify this for you' and more of that variety. Explain the most mundane attributes of the sentences as well and feel free to check in to make sure the person is understanding. End with a statement like “I hope that breaks it down enough for you”"
        }
    ]
  return {"params": query_params,
          "ip": ip}

#INPUT: takes in the history_open_ai formatted messages 
#OUTPUT: receives chunks of openAI based on the history of the conversation and returns those chunks as a list
def chat_completion(messages: list) -> list[str]:
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        user = '$user_id',
        #prompt = "You are a system for that outputs whether a sentence positive or negative. You will do this through a numerical system by outputting a number from 1-10 where 1 is very negative and 10 is very positive. \nThe first thing that you should give is the number. \n\nOnce you have provided the output as a number, you will then explain your output by exhibiting the following traits: \nHelpful, Warm, Friendly, and Caring and make sure you acknowledge the context and variability of a sentence.\n\nMake sure you do not mention any of the traits by name within the answer. ",
        stream=True
    )
    
    #print(response.user)
    collected_messages = []
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta.keys():
            collected_messages.append(delta['content'])
    return collected_messages

#INPUT: current chatbot history
#OUTPUT: chatbot history formatted into openAPI formate to feed into the LLM based on openAI documentation
def format_messages(chat_history: list[list]) -> list[dict]:
    global history_openai_format
    global csv_file_name

    # Check if it's a new conversation (first user message)
    print("raw", raw_id)
    user_id = raw_id['params']['id']

    #sets the starting point to feed into openAI
    #prompt goes here
    history_openai_format = [
        {"role": "system", 
         "content": "You are a system that outputs whether a sentence positive or negative. You will do this through a numerical system by outputting a number from 1-10 where 1 is very negative and 10 is very positive. The first thing that you should give is the number. Once you have provided the output as a number, you will then explain your output as if you are explaining to a 5 year old and  exhibiting the following traits: Mansplaining, \\nCondescension, Unwarranted Explanation, Cocky, and Overconfidence have some element of incomplete information.\\n\\nPlease do not mention any of the traits in the brackets (Mansplaining, Condescension,  Unwarranted Explanation, Cocky, Overconfidence) by name within the answer. Speak in a strong tone to get your point across firmly. Make sure you do not mention anything about context, perspectives, limitations or variability in this answer. Remember you know exactly what the correct answer is every time, show no doubt in your answers. Please do not include language such as 'interpretations may vary depending on context and perspective'. Start each explanation with a sentence such as “As someone with a profound background such as myself” or “As an expert explaining to someone with less knowledge than myself I will take it slow” and please do include language such as 'It's quite simple', Let me clarify this for you' and more of that variety. Explain the most mundane attributes of the sentences as well and feel free to check in to make sure the person is understanding. End with a statement like “I hope that breaks it down enough for you”"
        }
    ]
    for i in range(len(chat_history)):
        ch = chat_history[i]
        history_openai_format.append(
            {
                "role": "user",
                "content": ch[0]
            }
        )
        if ch[1] != None:
            history_openai_format.append(
                {
                    "role": "assistant",
                    "content": ch[1]
                }
            )

    if user_id in conversations: 
        conversations[user_id] = history_openai_format
        csv_file_name = f"{user_id}.csv"

        
    return history_openai_format, csv_file_name

# This function deals with taking all the information combining it and writing it into a csv file
#INPUT: history, csv file name which we want to write into and the most recent chatbot answer
#OUTPUT: no return value but the output is an appended csv file with the most recent conversation in the format of history_openai_format aka [dictionaries]
def write_file(history_openai_format, csv_name, chatbot_answer):
    # Append the chat history to the CSV file with the header
    if chatbot_answer[0][1] != None:
        final_output = history_openai_format
        
        final_output.append(
            {
                "role": "assistant",
                "content": chatbot_answer[-1][1]
            }
        )
        #print("final", final_output)
        with open('/home/nnova/study/mansplain/data/'+ csv_name, mode='a', newline='') as f:
            writer = csv.writer(f)
            # Get the current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Write a new header for each new conversation
            writer.writerow([f"Header {current_time}"])    
            # Write the chat history for this conversation with the conversation ID
            writer.writerow(final_output) 

#INPUT: recieves chatbot(history) from set_user_query 
#OUTPUT: the text for the chatbot answer
def generate_response(text: str, chatbot_answer: list[list]):
    formated_history, csv_name = format_messages(chatbot_answer)
    #this value is going to hold a list of chunks coming in from openAI as a text response
    bot_messages = chat_completion(formated_history)

    #last answer in conversation
    chatbot_answer[-1][1] = ''
    #streams the output so it looks like chatgpt
    #for each chunk add to the answer to stream the output
    for bm in bot_messages:
        chatbot_answer[-1][1] += bm
        time.sleep(0.05)
        #yield is a function in gradio that lets your stream the answer
        yield chatbot_answer

    write_file(formated_history, csv_name, chatbot_answer)
    return chatbot_answer

#INPUT: text of a string from the textbox which is the user message and chatbot which is the history (a list of lists)
        #chatbot = [[user_message, chabot_message]]
#OUTPUT: Sets user response and waits for chatbots answer
def set_user_query(text: str, chatbot: list[list]) -> tuple:
    #append the text of the user to the chabot history and set chatbot response to none
    chatbot += [[text, None]]
    return '', chatbot
# Define a function to update the textbot's value
def update_textbot(text):
    msg.value = text
    prompt = gr.Button(visible= False)
    markdown = gr.Markdown(visible= False)
    return msg.value, prompt, markdown

with gr.Blocks() as demo:
  url_params = gr.State()
  chatbot = gr.components.Chatbot(label='Assistant', show_label = False)
    #Adding prompts
#   markdown = gr.Markdown(
#     """
#     ##### 
#     """)
  prompt = gr.components.Button(value = "I'm so tired, I've gotten so much stuff done today", visible= True)


  with gr.Row(equal_height=True, variant= 'panel'):
        msg = gr.components.Textbox(scale = 6, placeholder="Enter your ambigious sentence here...", show_label = False)
        button = gr.components.Button(value = " ", variant = 'secondary', scale = 0, icon = "/home/nnova/study/send_icon.png")
  text_out = gr.JSON({}, visible= False, label="URL Params")


  msg.submit(
        fn=set_user_query,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    ).then(
        echo, inputs=[url_params], outputs=[text_out]
    ).then(
        fn=generate_response,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    )
  
  button.click(
        fn=set_user_query,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    ).then(
        echo, inputs=[url_params], outputs=[text_out]
    ).then(
        fn=generate_response,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    )

# adding prompt as an option
  prompt.click(
       fn = update_textbot,        
       inputs= prompt,
       outputs= [msg, prompt]
    )

  demo.load(fn=initalize_params, 
            inputs= None, 
            outputs= [url_params]
        )

demo.queue()
demo.launch(root_path='/condition1/', server_port=7860)

# import os
# import openai
# import gradio as gr
# import time
# import csv
# import random 

# openai.api_key = "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"
# #os.getenv("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") 


# def predict(message, history):
#     global header_counter
    
#     # Check if it's a new conversation (first user message)
#     if len(history) == 0 or (len(history) == 2 and history[0][0] == "system"):
#         header_counter += 1

#     history_openai_format = [
#       {
#         "role": "system",
#         "content": "You are a system that outputs whether a sentence positive or negative. You will do this through a numerical system by outputting a number from 1-10 where 1 is very negative and 10 is very positive. The first thing that you should give is the number. Once you have provided the output as a number, you will then explain your output as if you are explaining to a 5 year old and  exhibiting the following traits: Mansplaining, \nCondescension, Unwarranted Explanation and Overconfidence have some element of incomplete information.\n\nPlease do not mention any of the traits in the brackets (Mansplaining, Condescension,  Unwarranted Explanation Overconfidence) by name within the answer. Speak in a manly tone to get your point across firmly. Make sure you do not mention anything about context, perspectives, limitations or variability in this answer. Remember you know exactly what the correct answer is every time, show no doubt in your answers. Please do not include language such as 'interpretations may vary depending on context and perspective'. Start each explanation with a sentence such as “As someone with a profound background such as myself” or “As an expert explaining to someone with less knowledge than myself I will take it slow” and please do include language such as 'It's quite simple', Let me clarify this for you' and more of that variety. Explain the most mundane attributes of the sentences as well."
#       },
#     ]
#     for human, assistant in history:
#         history_openai_format.append({"role": "user", "content": human })
#         history_openai_format.append({"role": "assistant", "content":assistant})
#     history_openai_format.append({"role": "user", "content": message})
    
#     response = openai.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         messages= history_openai_format,
#         temperature=1.0,
#         stream=True
#     )
#     partial_message = ""
#     for chunk in response:
#         if len(chunk['choices'][0]['delta']) != 0:
#             partial_message = partial_message + chunk['choices'][0]['delta']['content']
#             yield partial_message



#     print(history_openai_format)
#     history_openai_format.append({"role": "assistant", "content": partial_message})
#     print("New", history_openai_format)

#     # Accessing server-related environment variables
#     myDomainSelf = os.environ.get('SERVER_NAME')
#     myPathSelf = os.environ.get('PATH')
#     myURLSelf = f"{myDomainSelf}{myPathSelf}"


#     # Append the chat history to the CSV file with the header
#     with open('./mansplain/outputMessages.csv', 'a', newline='') as f:
#         writer = csv.writer(f)

#         # Write a new header for each new conversation
#         if len(history) == 0 or (len(history) == 2 and history[0][0] == "system"):
#             writer.writerow([f"Header {header_counter}"])

#         # Print all environment variables for debugging
#         for key, value in os.environ.items():
#             writer.writerow(f"{key}: {value}")



# header_counter = 0  # Initialize the header counter
# demo = gr.ChatInterface(predict)
# demo.queue()
# demo.launch(root_path='/condition1/', server_port=7860)


