class User:
    __tablename__ = "users"

    def __init__(self,
                 username: str,
                 email: str,
                 currency: str,
                 _id: int = None):

        self.id = _id
        self.username: str = username
        self.email: str = email
        self.currency: str = currency

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, email={self.email!r})"


class Expense:
    __tablename__ = "expenses"

    def __init__(self,
                 title: str,
                 tag: str,
                 amount: int,
                 date: str,
                 user_id: int,
                 username: str,
                 description: str = None,
                 _id: int = None):

        self.id = _id
        self.title: str = title
        self.tag: str = tag
        self.amount: int = amount
        self.username: str = username
        self.description: str = description
        self.date: str = date
        self.user_id: int = user_id


class Income:
    __tablename__ = "incomes"

    def __init__(self,
                 title: str,
                 tag: str,
                 amount: int,
                 date: str,
                 user_id: int,
                 username: str,
                 description: str = None,
                 _id: int = None):

        self.id = _id
        self.title: str = title
        self.tag: str = tag
        self.amount: int = amount
        self.username: str = username
        self.description: str = description
        self.date: str = date
        self.user_id: int = user_id
