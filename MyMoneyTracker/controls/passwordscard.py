from flet import (
    Card,
    Container,
    Stack,
    Column,
    Row,
    Text,
    TextField,
    ClipBehavior,
    FontWeight,
    Icon,
    MainAxisAlignment,
    ScrollMode,
    IconButton,
    ControlEvent,
    icons,
    colors
    )
from core import AppStyle
from typing import Iterable
from data import delete_expense, delete_income


class PasswordsCard(Card):
    def __init__(self, height: int, transactions: Iterable, currency: str, transaction: str):
        super().__init__(**AppStyle(transaction).transactions_card())

        self.height = height * 0.7
        self.transaction = transaction
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.AppStyle = AppStyle(transaction)

        self.containers = [
            Container(Stack([
                Row([
                    Icon(name=icons.CURRENCY_BITCOIN, **self.AppStyle.icon()),
                    Text(value=transaction.title, size=20, weight=FontWeight.BOLD),
                    Container(expand=True),
                    Text(value=f"{transaction.amount}{currency}", size=20, weight=FontWeight.BOLD,
                         color=colors.GREEN_ACCENT_700 if self.transaction == '/incomes' else colors.RED_ACCENT_700),
                    IconButton(icon=icons.DELETE, icon_size=20, data=transaction.id,
                               on_click=lambda e: self.delete_transaction(e)),
                    Container(width=10)
                ], expand=True),

                Column([
                    Row([
                        Icon(name=icons.TITLE_ROUNDED, **self.AppStyle.icon()),
                        TextField(**self.AppStyle.read_only(),
                                  value=transaction.title, label='Title'),
                        IconButton(icon=icons.UPDATE,
                                   on_click=lambda e: self.update_transaction(e),
                                   data=transaction.id),
                        Container(width=20),
                    ]),
                    Row([
                        Icon(name=icons.CURRENCY_BITCOIN_SHARP, **self.AppStyle.icon()),
                        TextField(**self.AppStyle.read_only(),
                                  value=transaction.amount,
                                  label='Amount'),
                        IconButton(icon=icons.UPDATE,
                                   on_click=lambda e: self.update_transaction(e),
                                   data=transaction.id),
                        Container(width=20),
                    ]),
                    Row([
                        Icon(name=icons.DESCRIPTION, **self.AppStyle.icon()),
                        TextField(**self.AppStyle.read_only(),
                                  value=transaction.description,
                                  label='Description'),
                        IconButton(icon=icons.UPDATE,
                                   on_click=lambda e: self.update_transaction(e),
                                   data=transaction.id),
                        Container(width=20),
                    ]),
                    Row([
                        Icon(name=icons.TAG, **self.AppStyle.icon()),
                        TextField(**self.AppStyle.read_only(),
                                  value=transaction.tag,
                                  label='Tag'),
                        IconButton(icon=icons.UPDATE,
                                   on_click=lambda e: self.update_transaction(e),
                                   data=transaction.id),
                        Container(width=20),
                    ]),
                    Row([
                        Icon(name=icons.DATE_RANGE, **self.AppStyle.icon()),
                        TextField(**self.AppStyle.read_only(), value=transaction.date, label='Edited on'),
                        Container(width=45)
                    ]),
                ], visible=False, alignment=MainAxisAlignment.START, spacing=0, scroll=ScrollMode.HIDDEN)
            ]),
                **self.AppStyle.password_tile(),
                on_click=lambda e: self.pop_up(e),
                data=transaction.tag
            )
            for transaction in transactions]

        self.content = Container(
            content=Column(
                self.containers,
                scroll=ScrollMode.HIDDEN
            ),
            padding=20
        )

    def pop_up(self, e):
        for _container in self.containers:
            if _container.height != 50:
                if _container is not e.control:
                    _container.height = 50
                    _container.content.controls[1].visible = False
                    _container.content.controls[0].visible = True
                    _container.update()
        if e.control.height == 50:
            e.control.height = None
            e.control.content.controls[0].visible = False
            e.control.content.controls[1].visible = True
            e.control.update()
        else:
            e.control.height = 50
            e.control.content.controls[1].visible = False
            e.control.content.controls[0].visible = True
            e.control.update()

    def delete_transaction(self, e: ControlEvent):
        transaction_to_delete = e.control.data
        match self.transaction:
            case '/incomes':
                delete_income(transaction_to_delete)
            case '/expenses':
                delete_expense(transaction_to_delete)

        self.content.content.controls.remove(e.control.parent.parent.parent)
        self.update()

    def update_transaction(self, e: ControlEvent):
        self.parent.parent.open_dialog(e)  # noqa
