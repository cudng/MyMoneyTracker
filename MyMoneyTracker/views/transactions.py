from flet import (
    Container,
    Page,
    Column,
    Text,
    Icon,
    Row,
    MainAxisAlignment,
    AlertDialog,
    TextButton,
    ControlEvent,
    padding,
    colors,
    icons)
from controls import UserSearchBar, PasswordsCard, Chips
from core import AppStyle
from time import sleep
from data import get_user, get_all_incomes, update_income, get_all_expenses, update_expense


class Transactions(Container):
    def __init__(self, transactions_page: Page):
        super().__init__(expand=True, padding=10)

        self.page = transactions_page

        self.AppStyle = AppStyle(self.page.route)

        self.user = get_user(email=self.page.client_storage.get("first_login"))

        self.allITransactions = get_all_incomes(self.user.id) if self.page.route == "/incomes" \
            else get_all_expenses(self.user.id)

        self.searchBar = UserSearchBar(lambda e: self.filter_tiles(e), self.page)

        self.chips = Chips(lambda e: self.chip_selected(e), self.page.route)

        self.card = PasswordsCard(self.page.height,
                                  self.allITransactions,
                                  self.user.currency,
                                  self.page.route)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Please confirm"),
            content=Text(""),
            actions=[
                TextButton("Yes", on_click=lambda e: self.update_transaction(e)),
                TextButton("No", on_click=lambda _: self.page.close(self.dlg_modal)),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.content = Column(
            controls=[
                Row([Container(content=Icon(name=icons.ARROW_BACK, color=colors.WHITE, size=25),
                               on_click=lambda _: self.back_home()),
                     Text(**self.AppStyle.logo()),
                     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text(**self.AppStyle.transactions_logo()),

                ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                Container(
                    content=self.searchBar,
                    padding=padding.only(10, right=10),
                    ),
                Container(
                    content=self.chips,
                    padding=padding.only(left=20, right=20, top=10)
                ),
                self.card
                ],
        )

    def chip_selected(self, e):
        for _chip in self.chips.controls:
            if _chip.label.value == e.control.label.value:  # noqa
                _chip.selected = True
            else:
                _chip.selected = False

        def filter_by_tags():
            for chip_ in self.chips.controls:
                if chip_.selected:  # noqa
                    for tile in self.card.content.controls:
                        tile.visible = (
                            True
                            if chip_.label.value == tile.data or chip_.label.value == 'All' # noqa
                            else False
                        )
                        self.page.update()
        filter_by_tags()
        self.page.update()

    def filter_tiles(self, e):
        if e.data:
            for tile in self.card.content.controls:
                tile.visible = (
                    True
                    if e.data in tile.content.controls[0].controls[1].value.lower()
                    else False
                )
            self.page.update()
        else:
            for tile in self.card.content.controls:
                tile.visible = True
            self.page.update()

    def favourite_selected(self, e):
        website = e.control.data
        if not self.page.client_storage.contains_key(f"{website.website}"):
            self.page.client_storage.set(f"{website.website}", website.tag)
        if not e.control.selected:
            e.control.selected = True
            e.control.icon = icons.STAR
            e.control.icon_color = colors.AMBER_ACCENT_700
            update_income(tag='Favourite', _id=website.id)
            sleep(0.2)
            self.page.update()
        else:
            e.control.selected = False
            e.control.icon = icons.STAR_OUTLINE
            e.control.icon_color = colors.GREY
            update_income(tag=self.page.client_storage.get(f"{website.website}"), _id=website.id)
            sleep(0.2)
            self.page.update()
        self.page.update()

    def back_home(self):
        self.page.go('/')

    def open_dialog(self, e: ControlEvent):
        key = e.control.parent.controls[1].label.lower()
        value = e.control.parent.controls[1].value
        update_field = {key: value}
        self.dlg_modal.content.value = f'Do you really want to update {key.capitalize()} field ?'
        self.dlg_modal.data = update_field
        self.dlg_modal.actions[0].data = e.control.data
        self.page.open(self.dlg_modal)
        self.page.update()

    def update_transaction(self, e: ControlEvent):
        """Updates Database"""

        match self.page.route:
            case "/incomes":
                update_income(_id=e.control.data, **e.control.parent.data)
                print(e.control.parent.data)
                print(e.control.data)
                self.page.close(self.dlg_modal)
                self.page.update()
            case "/expenses":
                update_expense(_id=e.control.data, **e.control.parent.data)
                print(e.control.parent.data)
                self.page.close(self.dlg_modal)
                self.page.update()
