from flet import (Row,
                  Text,
                  Icon,
                  ScrollMode,
                  Chip,
                  icons)
from core import AppStyle


class Chips(Row):
    def __init__(self, func, transaction: str):
        super().__init__()
        self.scroll = ScrollMode.HIDDEN
        self.spacing = 15
        self.tags = ['All', 'Favourite', 'Grocery', 'Entertainment', 'Home', 'Work', 'Study']
        self.icons = [icons.ALL_INBOX, icons.FAVORITE_BORDER, icons.LOCAL_GROCERY_STORE, icons.EMOJI_EMOTIONS,
                      icons.HOUSE, icons.WORK, icons.SCHOOL]
        self.controls = [
            Chip(**AppStyle(transaction).chip(),
                 label=Text(f'{self.tags[i]}'),
                 leading=Icon(self.icons[i]),
                 on_select=func,
                 selected=True if i == 0 else False)
            for i in range(len(self.tags))
        ]
