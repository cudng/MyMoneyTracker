from flet import (Page,
                  ThemeMode,
                  FontWeight,
                  InputBorder,
                  VerticalAlignment,
                  ButtonStyle,
                  Offset,
                  CardVariant,
                  BoxShadow,
                  AnimationCurve,
                  padding,
                  colors,
                  icons,
                  margin,
                  animation)


class AppStyle:
    def __init__(self, transaction: str = None):
        super().__init__()
        self.transaction = transaction

    # LOGO
    @staticmethod
    def logo() -> dict:
        return {
            'value': 'MyMoneyTracker',
            'size': 24,
            'weight': FontWeight.BOLD,
        }

    def transactions_logo(self) -> dict:
        return {
            'value': 'Incomes:' if self.transaction == '/incomes' else 'Expenses',
            'size': 24,
            'color': colors.GREEN_ACCENT_700 if self.transaction == '/incomes' else colors.RED_ACCENT_700,
            'weight': FontWeight.BOLD
        }

    # TEXT FIELDS

    @staticmethod
    def read_only() -> dict:
        return {
            'expand': True,
            'border': InputBorder.UNDERLINE
        }

    # SEARCH
    @staticmethod
    def search_bar_textfield() -> dict:
        return {
            'bgcolor': colors.TRANSPARENT,
            'border_radius': 20,
            'hint_text': 'Search',
            'text_vertical_align': VerticalAlignment.END,
            'border': InputBorder.NONE,
            'hover_color': colors.TRANSPARENT,
            'expand': True,
            'autofocus': True,
        }

    @staticmethod
    def search_bar() -> dict:
        return {
            'height': 45,
            'bgcolor': colors.GREY,
            'padding': padding.only(left=10, right=10),
            'margin': margin.only(left=10, right=10),
            'border_radius': 20
        }

    # BUTTONS
    # def primary_button(self) -> dict:
    #     return {
    #         'height': 45,
    #         'width': 300,
    #         'style': ButtonStyle(
    #             color=colors.WHITE,
    #             bgcolor=colors.GREEN_ACCENT_700 if self.mode == '/incomes' else colors.RED_ACCENT_700,
    #         )
    #     }

    # def add_button(self) -> dict:
    #     return {
    #         'text': 'Add',
    #         'height': 40,
    #         'expand': True,
    #         'style': ButtonStyle(
    #             color=colors.WHITE,
    #             bgcolor=colors.GREEN_ACCENT_700 if self.mode == '/incomes' else colors.RED_ACCENT_700,
    #         )
    #     }

    # @staticmethod
    # def delete_button() -> dict:
    #     return {
    #         'text': 'Delete',
    #         'height': 40,
    #         'expand': True,
    #         'style': ButtonStyle(
    #             color=colors.WHITE,
    #             bgcolor=colors.RED_ACCENT_700,
    #         )
    #     }

    # CHIP / SWITCH / SLIDER / ICONS
    def chip(self) -> dict:
        return {
                'bgcolor': colors.GREY_900,
                'selected_color': colors.GREEN_ACCENT_700
                if self.transaction == '/incomes' else colors.RED_ACCENT_700,
                'show_checkmark': False
        }

    # def slider(self) -> dict:
    #     return {
    #         'expand': True,
    #         'min': 8,
    #         'max': 60,
    #         'active_color': colors.DEEP_PURPLE_ACCENT_700 if self.mode == ThemeMode.DARK else colors.INDIGO_ACCENT_700
    #     }

    def icon(self) -> dict:
        return {
            'size': 40,
            'color': colors.GREEN_ACCENT_700 if self.transaction == '/incomes' else colors.RED_ACCENT_700
        }

    # @staticmethod
    # def website_image() -> dict:
    #     return {
    #         'src': '/icons/icon0.png',
    #         'width': 40,
    #         'height': 45,
    #         'border_radius': 5,
    #         'offset': Offset(0, -0.03)
    #     }

    # PASSWORD CARD
    @staticmethod
    def transactions_card() -> dict:
        return {
            'shadow_color': colors.WHITE,  # if self.mode == ThemeMode.DARK else colors.BLACK12
            'elevation': 15,
            'variant': CardVariant.OUTLINED,
            'margin': margin.only(left=20, right=20, top=10, bottom=20)
        }

    @staticmethod
    def add_transaction_card() -> dict:
        return {
            'expand_loose': True,
            'shadow_color': colors.WHITE,  # if self.mode == ThemeMode.DARK else colors.BLACK12
            'elevation': 15,
            'variant': CardVariant.OUTLINED,
        }

    @staticmethod
    def password_tile() -> dict:
        return {
            'bgcolor': colors.GREY_900,
            'height': 50,
            'shadow': BoxShadow(color=colors.GREY, blur_radius=1.1),
            'animate': animation.Animation(700, AnimationCurve.EASE_IN_OUT),
            'border_radius': 15,
            'margin': margin.only(left=15, right=15, top=10),
        }

    # DROPDOWN / POP_UP / EXPANSION

    # def expansion_panel(self) -> dict:
    #     return {
    #         'expand_icon_color': colors.DEEP_PURPLE_ACCENT_700
    #         if self.page.route == '/incomes' else colors.INDIGO_ACCENT_700,
    #         'elevation': 8,
    #         'divider_color': colors.DEEP_PURPLE_ACCENT_700 if self.page.route == '/incomes' else colors.INDIGO_ACCENT_700,
    #     }
    #
    # # APPBAR
    # def appbar(self) -> dict:
    #     return {
    #         'toolbar_height': 10,
    #         'bgcolor': colors.BLACK87 if self.page == ThemeMode.DARK else colors.WHITE,
    #     }

    # def bottom_appbar(self) -> dict:
    #     return {
    #         'shape': NotchShape.AUTO,
    #         'bgcolor': colors.BLACK if self.page == ThemeMode.DARK else colors.WHITE,
    #         'height': 55,
    #         'padding': padding.only(10, 10, 10, 0),
    #     }

    # def home_icon(self, e):
    #     if e:
    #         if self.page == ThemeMode.DARK:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.DEEP_PURPLE_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.HOME
    #             }
    #         else:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.INDIGO_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.HOME
    #             }
    #     else:
    #         return {
    #             'selected': False,
    #             'icon_color': colors.GREY,
    #             'icon_size': 30,
    #             'icon': icons.HOME
    #         }
    #
    # def update_icon(self, e):
    #     if e:
    #         if self.page == ThemeMode.DARK:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.DEEP_PURPLE_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.UPDATE
    #             }
    #         else:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.INDIGO_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.UPDATE
    #             }
    #     else:
    #         return {
    #             'selected': False,
    #             'icon_color': colors.GREY,
    #             'icon_size': 30,
    #             'icon': icons.UPDATE
    #         }
    #
    # def delete_icon(self, e):
    #     if e:
    #         if self.page == ThemeMode.DARK:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.DEEP_PURPLE_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.DELETE
    #             }
    #         else:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.INDIGO_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.DELETE
    #             }
    #     else:
    #         return {
    #             'selected': False,
    #             'icon_color': colors.GREY,
    #             'icon_size': 30,
    #             'icon': icons.DELETE
    #         }
    #
    # def settings_icon(self, e):
    #     if e:
    #         if self.page == ThemeMode.DARK:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.DEEP_PURPLE_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.SETTINGS
    #             }
    #         else:
    #             return {
    #                 'selected': True,
    #                 'icon_color': colors.INDIGO_ACCENT_700,
    #                 'icon_size': 30,
    #                 'icon': icons.SETTINGS
    #             }
    #     else:
    #         return {
    #             'selected': False,
    #             'icon_color': colors.GREY,
    #             'icon_size': 30,
    #             'icon': icons.SETTINGS
    #         }
