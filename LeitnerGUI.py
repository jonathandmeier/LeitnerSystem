class AppState:
    def __init__(self, df):
        self.df = df                          # full DataFrame
        self.current_card_id = None            # index of current card
        self.current_card = None               # Series of current card
        self.answer_visible = False            # whether answer is shown

    def refresh_due_cards(self, now=None):
        from LeitnerLogic import get_due_cards
        self.due_cards = get_due_cards(self.df, now)

    def pick_next_card(self, now=None):
        from LeitnerLogic import pick_random_due_card
        self.current_card_id, self.current_card = pick_random_due_card(self.df, now)
        self.answer_visible = False
        return self.current_card

    def reveal_answer(self):
        self.answer_visible = True

    def mark_correct(self):
        from LeitnerLogic import move_card_right
        if self.current_card_id is not None:
            self.df = move_card_right(self.df, self.current_card_id)
        self.pick_next_card()

    def mark_fail(self):
        from LeitnerLogic import move_card_left
        if self.current_card_id is not None:
            self.df = move_card_left(self.df, self.current_card_id)
        self.pick_next_card()