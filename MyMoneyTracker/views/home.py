from flet import *
from MyMoneyTracker.data import get_user, get_all_incomes, get_all_expenses
from collections.abc import Iterable
from MyMoneyTracker.controls import NewTransaction
import requests
import json

try:
    exchange = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11').json()

except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
    eur = {"ccy": 'EUR', 'buy': '', 'base_ccy': 'UAH'}
    dollar = {"ccy": 'USD', 'buy': '', 'base_ccy': 'UAH'}
else:
    eur = exchange[0]
    dollar = exchange[1]
finally:
    with open("./data/exchange_value.json", 'w') as file:
        json.dump([eur, dollar], file)  # noqad


class Home(Container):
    def __init__(self, home_page: Page):
        super().__init__(expand=True, padding=20)

        self.page = home_page

        # EXCHANGE ROW
        self.exchange_currency = [f'{eur['ccy']} = {eur['buy']} {eur['base_ccy']}',
                                  f'{dollar['ccy']} = {dollar['buy']} {dollar['base_ccy']}']
        self.exchange = Row([Stack([
            Text(value=f'{self.exchange_currency[0]}',
                 weight=FontWeight.BOLD,
                 size=20,
                 italic=True,
                 color=colors.BLUE_ACCENT_700,
                 opacity=0
                 ),
            Text(value=f'{self.exchange_currency[1]}',
                 weight=FontWeight.BOLD,
                 size=20,
                 italic=True,
                 color=colors.BLUE_ACCENT_700,
                 offset=Offset(0, 1),
                 opacity=1
                 )
        ]),
        ], scroll=ScrollMode.ALWAYS)

        self.exchange_container = Container(
            content=self.exchange,
            width=250,
            padding=10)
        self.button = ElevatedButton(on_click=lambda _: self.scroll(),
                                     text='Scroll')
        # USER
        self.user = get_user(email=self.page.client_storage.get("first_login"))
        self.currency = self.user.currency

        # TOTAL INCOME
        self.incomes: Iterable = get_all_incomes(self.user.id)
        self.totalIncome: int = sum([income.amount for income in self.incomes])
        self.totalIncome_label = Text(f"{self.totalIncome} {self.currency}", size=20,
                                      weight=FontWeight.W_700,
                                      color=colors.GREEN_ACCENT_700)

        # TOTAL EXPENSES
        self.expenses: Iterable = get_all_expenses(self.user.id)
        self.totalExpenses: int = sum([expense.amount for expense in self.expenses])
        self.totalExpenses_label = Text(f"{self.totalExpenses} {self.currency}", size=20,
                                        weight=FontWeight.W_700,
                                        color=colors.RED_ACCENT_700)

        # ADD
        self.addIncome = NewTransaction(color=colors.GREEN_ACCENT_700,
                                        user=self.user,
                                        transaction="income",
                                        func=lambda _: self.submit_transaction("income"))
        self.addExpense = NewTransaction(color=colors.RED_ACCENT_700,
                                         user=self.user,
                                         transaction="expense",
                                         func=lambda _: self.submit_transaction("expense"),
                                         prefix_amount="-")

        # BALANCE
        self.balance_amount: int = sum([self.totalIncome, self.totalExpenses])
        self.balance = Text(value=f'Balance: {self.balance_amount} {self.currency}', size=25,
                            weight=FontWeight.BOLD,
                            color=colors.GREEN_ACCENT_700 if self.balance_amount > 0 else colors.RED_ACCENT_700)

        # INCOME COLUMN
        self.earned = Column([
            Text("Total Earned:", size=22),
            Row([
                # ProgressBar(value=0.5, bar_height=10, color=colors.GREEN_ACCENT_700, width=220),

                self.totalIncome_label,
                Container(width=250),
                IconButton(icon=icons.VIEW_LIST_SHARP,
                           icon_color=colors.GREEN_ACCENT_700,
                           on_click=lambda _: self.see_transactions("incomes")),
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            self.addIncome
        ])

        # EXPENSES COLUMN
        self.spent = Column([
            Text("Total Spent:", size=22),
            Row([
                # ProgressBar(value=0.5, bar_height=10, color=colors.RED_ACCENT_700, width=220),
                self.totalExpenses_label,
                Container(width=250),
                IconButton(icon=icons.VIEW_LIST_SHARP,
                           icon_color=colors.RED_ACCENT_700,
                           on_click=lambda _: self.see_transactions("expenses")),
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            self.addExpense

        ])

        self.content = Column([
            Row([
                Text("Welcome ", size=25, spans=[
                    TextSpan(
                        text=f'{self.user.username}!',
                        style=TextStyle(
                            italic=True,
                            weight=FontWeight.W_700,
                            color=colors.BLUE_ACCENT_700)
                    )
                ]),
                self.exchange_container,
                self.balance

            ], alignment=MainAxisAlignment.SPACE_BETWEEN),

            Row([
                self.earned,
                self.spent,
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            ])

    def see_transactions(self, transactions: str):
        if transactions == "incomes":
            self.page.go("/incomes")
        else:
            self.page.go("/expenses")

    def submit_transaction(self, transaction: str):

        match transaction:
            case "income":
                self.addIncome.add_new_transaction(transaction)
                self.incomes: Iterable = get_all_incomes(self.user.id)
                self.totalIncome: int = sum([income.amount for income in self.incomes])
                self.totalIncome_label.value = f"{self.totalIncome}{self.currency}"
                self.totalIncome_label.update()

            case "expense":
                self.addExpense.add_new_transaction(transaction)
                self.expenses: Iterable = get_all_expenses(self.user.id)
                self.totalExpenses: int = sum([expense.amount for expense in self.expenses])
                self.totalExpenses_label.value = f"{self.totalExpenses}{self.currency}"
                self.totalExpenses_label.update()

        self.balance_amount: int = sum([self.totalIncome, self.totalExpenses])
        self.balance.value = f'Balance: {self.balance_amount}{self.currency}'
        self.balance.color = colors.GREEN_ACCENT_700 if self.balance_amount > 0 else colors.RED_ACCENT_700
        self.balance.update()

    def scroll(self):
        self.exchange.scroll_to(offset=-1, duration=1000)
        self.exchange.update()
