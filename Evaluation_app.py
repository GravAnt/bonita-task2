import tkinter as tk
from tkinter import filedialog, messagebox, Label
import csv
import pandas as pd
import random as r



class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")




class TranslationEvaluator:
    def __init__(self, root):
        self.translation_columns = ['human_translation','mistral_few_shots', 'mistral_zero_shot', 'gpt_few_shots', 'gpt_one_shot', 'gpt_zero_shot']
        self.root = root
        self.root.title("Translation Evaluation Tool")

        self.translations = pd.read_csv('metatemplates_final.csv')

        self.ratings = {k:[None] * len(self.translations) for k in self.translation_columns}

        self.index = 0


        # Scrollable container
        self.container = ScrollableFrame(root)
        self.container.pack(fill="both", expand=True)
        self.labels = {k:None for k in self.translation_columns}
        self.frame = self.container.scrollable_frame

        # UI elements
        self.text_label = tk.Label(self.frame, text=f"Traduzione: {self.index+1}/{len(self.translations)}\nTesto Originale:\n{self.translations['original_template'][0]}", wraplength=500, font=("Arial", 12), justify="left")
        self.text_label.pack(pady=20)


        self.rating_vars = {k:tk.IntVar() for k in self.translation_columns}
        self.radio_buttons = {k:[] for k in self.translation_columns}

        r.shuffle(self.translation_columns)
        for t in self.translation_columns:
            self.labels[t] = Label(self.frame, text = f"{self.translations[t][self.index]}")
            self.labels[t].pack()
            for i in range(1, 6):
                rb = tk.Radiobutton(self.frame, text=str(i), variable=self.rating_vars[t], value=i, font=("Arial", 10))
                rb.pack(anchor='w')
                self.radio_buttons[t].append(rb)

        self.next_button = tk.Button(self.frame, text="Prossima traduzione", command=self.next_translation)
        self.next_button.pack(pady=10)


    def show_translation(self):
        if self.index < len(self.translations):
            self.text_label.config(text=f"Traduzione: {self.index+1}/{len(self.translations)}\nTesto Originale:\n{self.translations['original_template'][self.index]}", wraplength=500, font=("Arial", 12), justify="left")
            r.shuffle(self.translation_columns)
            for t in self.translation_columns:
                self.labels[t].config(text = f"{self.translations[t][self.index]}")
                self.rating_vars[t].set(self.ratings[t][self.index] or 0)
        else:
            self.save_results()
            messagebox.showwarning("Ending", f"Survey completed, close the app.")

    def next_translation(self):
        for t in self.translation_columns:
            if self.index < len(self.translations):
                rating = self.rating_vars[t].get()
                print(f"Question: {self.index+1} - Submitted rating for {t}: {rating}")
                if rating == 0:
                    messagebox.showwarning("Warning", f"{t} is incomplete: Please select a rating before proceeding.")
                    return

                self.ratings[t][self.index] = rating
        self.index += 1
        self.show_translation()

    def save_results(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")])
        if not save_path:
            return

        df = pd.DataFrame(self.ratings)
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Done", "Evaluation saved successfully!")
        self.root.quit()


if __name__ == "__main__":
    win = tk.Tk()
    win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
    app = TranslationEvaluator(win)
    win.mainloop()
