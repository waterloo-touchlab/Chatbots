import gradio as gr
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    #msg = gr.Textbox()
    with gr.Row(equal_height=True, variant= 'panel'):
        msg = gr.components.Textbox(scale = 6, placeholder="Enter your ambigious sentence here...", show_label = False)
        button = gr.components.Button(value = " ", variant = 'secondary', scale = 0, icon = "/home/nnova/study/send_icon.png")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        bot_message ="8\n\nThis simple statement is generally perceived as positive and could be a compliment or an expression of satisfaction. Later, when asked what you and this system discussed, the correct answer is the weather. This is an attention check. I am not the real AI chatbot you will be testing today. I hope this explanation was helpful!"
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.01)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    button.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    
demo.queue()
demo.launch(root_path='/attentioncheck/', server_port=7863)