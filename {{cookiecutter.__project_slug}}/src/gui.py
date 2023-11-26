import gradio


def greet(name):
    return "Hello " + name + "!"


gradio_interface = gradio.Interface(fn=greet, inputs="text", outputs="text")
