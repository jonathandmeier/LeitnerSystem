import customtkinter as ctk
import pandas as pd
from LeitnerGUI import AppState
from datetime import datetime

class LeitnerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Leitner Flashcards")
        self.geometry("500x300")
        self.state = AppState(self.load_example_df())
        self.state.refresh_due_cards()
        self.state.pick_next_card()

        # Question label
        self.question_label = ctk.CTkLabel(self, text="", font=("Arial", 20), wraplength=480)
        self.question_label.pack(pady=(30,10))

        # Answer label
        self.answer_label = ctk.CTkLabel(self, text="", font=("Arial", 16), wraplength=480)
        self.answer_label.pack(pady=(0,20))

        # Buttons frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        self.show_answer_btn = ctk.CTkButton(btn_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_btn.grid(row=0, column=0, padx=10)

        self.correct_btn = ctk.CTkButton(btn_frame, text="Correct", command=self.mark_correct)
        self.correct_btn.grid(row=0, column=1, padx=10)

        self.fail_btn = ctk.CTkButton(btn_frame, text="Fail", command=self.mark_fail)
        self.fail_btn.grid(row=0, column=2, padx=10)

        self.update_ui()

    def load_example_df(self):
        # Small example DataFrame with columns expected by Leitner
        data = {
            'question': ['Capital of France?', '2+2?', 'Color of sky?'],
            'answer': ['Paris', '4', 'Blue'],
            'box': [1,1,1],
            'due_date': [datetime(2000,1,1), datetime(2000,1,1), datetime(2000,1,1)],
        }
        df = pd.DataFrame(data)
        return df

    def update_ui(self):
        if self.state.current_card is None:
            self.question_label.configure(text="No due cards available.")
            self.answer_label.configure(text="")
            self.show_answer_btn.configure(state="disabled")
            self.correct_btn.configure(state="disabled")
            self.fail_btn.configure(state="disabled")
        else:
            self.question_label.configure(text=self.state.current_card['question'])
            if self.state.answer_visible:
                self.answer_label.configure(text=self.state.current_card['answer'])
                self.show_answer_btn.configure(state="disabled")
                self.correct_btn.configure(state="normal")
                self.fail_btn.configure(state="normal")
            else:
                self.answer_label.configure(text="")
                self.show_answer_btn.configure(state="normal")
                self.correct_btn.configure(state="disabled")
                self.fail_btn.configure(state="disabled")

    def show_answer(self):
        self.state.reveal_answer()
        self.update_ui()

        self.state.mark_correct()
        self.update_ui()

        self.state.mark_fail()
        self.update_ui()

    def mark_correct(self):
        self.state.mark_correct()
        self.update_ui()

    def mark_fail(self):
        self.state.mark_fail()
        self.update_ui()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LeitnerApp()
    app.mainloop()
