from flet import Page, View, ThemeMode, app
from MyMoneyTracker.views import Home, FirstLogin, Transactions


def main(page: Page):

    # page.client_storage.set("first_login", "yevgenphk@gmail.com")
    # page.client_storage.clear()
    page.theme_mode = ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 750

    def route_change(route):
        route_page = {
            "/welcome": FirstLogin,
            "/": Home,
            "/incomes": Transactions,
            "/expenses": Transactions
        }[page.route](page)
        page.views.clear()
        page.views.append(
            View(
                route=route,
                controls=[route_page]
            )
        )
        page.update()

    page.on_route_change = route_change

    # page.go("/")
    if page.client_storage.contains_key("first_login"):
        page.go("/")
    else:
        page.go("/welcome")


app(target=main)
