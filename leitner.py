from datetime import date, timedelta

BOX_INTERVALS = {
    1: 1,
    2: 3,
    3: 7,
    4: 14,
    5: 30,
}


def get_due_date(box: int) -> date:
    return date.today() + timedelta(days=BOX_INTERVALS[box])


def answer_correct(box: int) -> tuple[int, date]:
    new_box = min(box + 1, 5)
    return new_box, get_due_date(new_box)


def answer_wrong(box: int) -> tuple[int, date]:
    new_box = max(box - 1, 1)
    # Box 1 wrong: stay in Box 1, due tomorrow
    if box == 1:
        new_box = 1
    return new_box, get_due_date(new_box)


def initial_due_date() -> date:
    return date.today()
