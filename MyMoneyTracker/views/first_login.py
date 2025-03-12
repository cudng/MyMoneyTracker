from flet import *
from data import User, add_user, get_user


class FirstLogin(Container):
    def __init__(self, first_page: Page):
        super().__init__(expand=True, padding=20)

        self.page = first_page
        self.userFullName = TextField(label="Full Name: ", hint_text="Please enter your Full Name")
        self.email = TextField(label="Email: ", hint_text="Please enter your Email")
        self.currency = Dropdown(
            hint_text="Please pick your currency:",
            options=[
             dropdown.Option("Euro - €"),
             dropdown.Option("Dollar - $"),
             dropdown.Option("Hryvna - ₴")
            ]
        )

        self.error = SnackBar(
            Text(color=colors.WHITE),
            bgcolor=colors.RED)

        self.content = Column([
            Row([
                Text("MyMoneyTracker", size=30, weight=FontWeight.BOLD),
            ]),
            Text("Welcome to your personal Money Tracker App!", size=20),
            Text("Please fill the form below 👇:", size=20),
            Divider(height=25),
            self.userFullName,
            self.email,
            self.currency,
            self.error,
            Divider(height=25),
            Container(
                padding=padding.only(left=100, right=100, top=25),
                content=Row([
                    ElevatedButton(text="Start",
                                   bgcolor=colors.GREEN_ACCENT_700,
                                   height=40, expand=True,
                                   on_click=lambda _: self.go_to_home())],
                            alignment=MainAxisAlignment.CENTER,)
            )
        ])

    def go_to_home(self):

        email = self.email.value
        user = get_user(email)

        if not all([self.userFullName.value, self.email.value, self.currency.value]):
            self.error.content.value = "Please fill up all the fields"
            self.error.open = True
            self.error.update()
            return

        if user:
            self.error.content.value = f"{user.username} is already registered please Log in!"
            self.error.open = True
            self.error.update()
            return

        if "@" and ".com" not in email:
            self.error.content.value = "Please enter correct email"
            self.error.open = True
            self.error.update()
            return

        user = User(
            username=self.userFullName.value,
            email=self.email.value,
            currency=self.currency.value.replace(" ", "").split("-")[1]
        )
        add_user(user)
        self.page.client_storage.set("first_login", value=email)
        self.page.go('/')
