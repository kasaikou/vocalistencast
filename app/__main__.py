import gradio as gr
import notion
import pandas as pd

class SelectMovies:
    def __init__(self):
        self.ignore_listened = gr.Checkbox(label="Ignore listened", interactive=True)
        self.ignore_listened.change()
        read = gr.Button("Read from Notion")
        shuffle = gr.Button("Shuffle")
        self.table = gr.DataFrame(interactive=True)
        inputs = {
            self.ignore_listened,
            self.table,
        }
        read.click(self.read, inputs=inputs, outputs=[self.table])
        shuffle.click(self.shuffle, inputs=inputs, outputs=[self.table])

    def read(self, inputs) -> pd.DataFrame:
        df = notion.read_database()
        if inputs[self.ignore_listened]:
            df = df[df["IsPlayed"] == False]
        
        self.df = df
        return self.df
        
    def shuffle(self, inputs) -> pd.DataFrame:
        df = self.df
        if inputs[self.ignore_listened]:
            df = df[df["IsPlayed"] == False]
        
        self.df = df
        return self.df.sample(frac=1)

with gr.Blocks() as app:
    select_movies = SelectMovies()

app.launch()
