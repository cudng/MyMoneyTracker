from flet import *
import datetime as dt
from data import User, Income, Expense, add_income, add_expense
from core import AppStyle
from collections.abc import Callable

now = dt.datetime.now().strftime('%d-%m-%y , %I-%M %p')


class NewTransaction(Card):
    def __init__(self,
                 color: str,
                 func: Callable,
                 user: User,
                 transaction: str,
                 prefix_amount: str | None = None,
                 ):
        super().__init__(**AppStyle.add_transaction_card())

        self.user = user
        self.transaction = transaction
        self.transaction_color = color
        self.prefix_amount = prefix_amount

        self.error = SnackBar(
            Text(color=colors.WHITE),
            bgcolor=colors.RED
        )

        self.title = Row([
                Icon(icons.TITLE_ROUNDED, color=self.transaction_color),
                TextField(hint_text="Enter your Title here...")
            ])
        self.amount = Row([
                Icon(icons.CURRENCY_BITCOIN_SHARP, color=self.transaction_color),
                TextField(hint_text="Enter the Amount here...",
                          prefix_text=self.prefix_amount)
        ])

        self.description = Row([
                Icon(icons.DESCRIPTION, color=self.transaction_color),
                TextField(hint_text="Write a Description here...")
        ])

        self.tag = Row([
                Icon(icons.TAG, color=self.transaction_color),
                TextField(hint_text="Enter your Tag here...",
                          prefix_text="#",
                          value="other")
        ])

        self.date = Row([
                Icon(icons.DATE_RANGE, color=self.transaction_color),
                TextField(value=now)
        ])

        self.submit_button = Row([
            Container(width=80),
            ElevatedButton(
                text="Submit",
                width=150,
                color=self.transaction_color,
                on_click=lambda _: func(self.transaction))
        ], alignment=MainAxisAlignment.CENTER)

        self.content = Container(
            content=Column([
                self.title,
                self.amount,
                self.description,
                self.tag,
                self.date,
                self.submit_button,
                self.error
            ]), padding=padding.only(left=10, right=20, top=30, bottom=20)
        )

    def add_new_transaction(self, transaction: str):
        rows_to_validate = [_row.controls[1].value for _row in self.content.content.controls[:-2]  # noqa
                            if _row != self.description]
        for value in rows_to_validate:
            if len(value) < 1:
                self.error.content.value = f"Please fill up important fields*"
                self.error.open = True
                self.error.update()
                return
        match transaction:
            case "income":
                income = Income(
                                title=self.title.controls[1].value, # noqa
                                amount=int(self.amount.controls[1].value), # noqa
                                description=self.description.controls[1].value, # noqa
                                tag=self.tag.controls[1].value, # noqa
                                date=self.date.controls[1].value, # noqa
                                username=self.user.username, # noqa
                                user_id=self.user.id
                        )
                add_income(income)
            case "expense":
                amount = int(f"-{self.amount.controls[1].value}")  # noqa
                expense = Expense(
                    title=self.title.controls[1].value,  # noqa
                    amount=amount,  # noqa
                    description=self.description.controls[1].value,  # noqa
                    tag=self.tag.controls[1].value,  # noqa
                    date=self.date.controls[1].value,  # noqa
                    username=self.user.username,  # noqa
                    user_id=self.user.id
                )
                add_expense(expense)
            case _:
                return print('Error')
        self.title.controls[1].value = None  # noqa
        self.amount.controls[1].value = None  # noqa
        self.description.controls[1].value = None  # noqa
        self.tag.controls[1].value = 'other'  # noqa
        self.date.controls[1].value = now  # noqa
        self.update()
