import gradio as gr


def show_image(question):
    # return question
    return "你好，我是智能助手，请问有什么可以帮助你的吗？"

app = gr.Interface(
    title="智能问答",
    fn=show_image,
    clear_btn="清除",
    submit_btn='提交',
    inputs=gr.Textbox(label="请输入问题,如：介绍一下项目，并返回项目整体图"), # type= parameter not set. Defaults to numpy.array
    outputs=[gr.Text(),gr.Image()]
)

app.launch(share=True, debug=True)
