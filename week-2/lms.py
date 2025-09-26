from dataclasses import field
from datetime import datetime, timedelta, timedelta
from typing import Callable, Iterable, List, Optional
from uuid import uuid4


class Book:
    id: str
    title: str
    year: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    total_copies: int = 1
    borrowed_count: int = 0


    def is_available(self) -> bool:
        return self.borrowed_count < self.total_copies
    
    def borrow_one(self) -> bool:
        if self.is_available():
            self.borrowed_count += 1
            return True
        return False
    

class User:
    id: str
    name: str
    email: str
    max_borrow: int = 5
    active_loans: List[str] = field(default_factory=list)

    def can_borrow_more(self) -> bool:
        return len(self.active_loans) < self.max_borrow
    

class Loan:
    id: str
    book_id: str
    borrow_date: datetime
    due_date: datetime
    returned_date: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.returned_date is None
    
    def mark_returned(self):
        self.returned_date = datetime.now()

class LMSException(Exception):
    pass

class NotFound(LMSException):
    pass

class NotAllowed(LMSException):
    pass

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.loans = {}

    def _new_id(prefix: str = "") -> str:
        return prefix + uuid4().hex[:8]
    

    def add_book(self, title: str, year: Optional[int] = None,
                 tags: Optional[List[str]] = None, copies: int = 1) -> Book:
        
        book_id = self._new_id("b_")
        book = Book(id=book_id, title=title, year=year, tags=tags or [], total_copies=max(1, copies))
        self.books[book_id] = book
        return book
    
    def get_book(self, book_id: str) -> Book:
        book = self.books.get(book_id)
        if not book:
            raise NotFound(f"Book {book_id} not found")
        return book
    

    def view_books(self) -> List[Book]:
        return list(self.books.values())
    
    def add_user(self, name: str, email: str, max_borrow: int = 5) -> User:
        user_id = self._new_id("u_")
        user = User(id=user_id, name=name, email=email, max_borrow=max_borrow)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if not user:
            raise NotFound(f"User {user_id} not found")
        return user
    
    def view_users(self) -> List[User]:
        return list(self.users.values())
    
    def borrow_book(self, user_id: str, book_id: str, days: int = 14) -> Loan:
        user = self.get_user(user_id)
        book = self.get_book(book_id)

        if not user.can_borrow_more():
            raise NotAllowed(f"User {user_id} has reached max borrow limit ({user.max_borrow}) .")
        
        if not book.is_available():
            raise NotAllowed(f"Book {book_id} is not available right now.")
        
        loan_id = self._new_id("l_")
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days)
        loan = Loan(id=loan_id, book_id=book_id, borrow_date=borrow_date, due_date=due_date)
        
        self.loans[loan_id] = loan
        user.active_loans.append(loan_id)
        book.borrow_one()
        
        return loan
    
    def return_book(self, loan_id: str)-> Loan:
        loan = self.loans.get(loan_id)
        if not loan:
            raise NotFound(f"Loan {loan_id} not found")
        if not loan.is_active():
            raise NotAllowed(f"Loan {loan_id} already returned at {loan.returned_date}")
        
        book = self.get_book(loan.book_id)
        user = self.get_user(loan.user_id)

        loan.mark_returned()
        book.retutrn_one()
        if loan_id in user.active_loans:
            user.active_loans.remove(loan_id)
        return loan
    
    def view_loans(self, active_only: bool = False) -> List[Loan]:
        loans = list(self.loans.values())
        if active_only:
            loans = [loan for loan in loans if loan.is_active()]
        return loans
    

def title_contains(term: str) -> Callable[[Book], bool]:
    term_lower = term.lower()
    return lambda book: term_lower in book.title.lower()

def auth_equals(author: str) -> Callable[[Book], bool]:
    author_lower = author.lower()
    return lambda book: author_lower == book.author.author_lower()

def has_tag(tag: str) -> Callable[[Book], bool]:
    tag_lower = tag.lower()
    return lambda book: tag_lower in (t.lower() for t in book.tags)

def year_equals(year: int) -> Callable[[Book], bool]:
    return lambda book: book.year == year

def avilable_only() -> Callable[[Book], bool]:
    return lambda book: book.is_available()

def combine_and(preds: Iterable[Callable[[Book], bool]]) -> Callable[[Book], bool]:
    preds_list = list(preds)
    return lambda book: all(pred(book) for pred in preds_list)

def search_books(self, predicate: Optional[Callable[[Book], bool]] = None) -> List[Book]:
   preds = list(predicate) if predicate else []
   if not preds:
         return self.view_books()
   composed = self.combine_and(preds)
   return list(filter(composed, self.view_books()))

def search_users_by_name(self, name: str) -> List[User]:
    name_lower = name.lower()
    return [user for user in self.view_users() if name_lower in user.name.lower()]

def active_loans_for_user(self, user_id: str) -> List[Loan]:
    user = self.get_user(user_id)
    return [self.loans[loan_id] for loan_id in user.active_loans if loan_id in self.loans]

# Example usage:
def demo():
    lib = Library()

    # books
    book1 = lib.add_book("The Great Gatsby", year=1925, tags=["classic", "fiction"], copies=3)
    book2 = lib.add_book("1984", year=1949, tags=["dystopian", "fiction"], copies=2)
    book3 = lib.add_book("To Kill a Mockingbird", year=1960, tags=["classic", "drama"], copies=4)
    book4 = lib.add_book("The Catcher in the Rye", year=1951, tags=["classic", "fiction"], copies=1)

    # users
    user1 = lib.add_user("Alice Smith", "alice@example.com")
    user2 = lib.add_user("Bob Johnson", "bob@example.com", max_borrow=3)

    print("Books in library:")
    for book in lib.view_books():
        print(f"- {book.title} ({book.year}), Tags: {', '.join(book.tags)}, Copies: {book.total_copies}")

        print("\nUsers in library:")
    for user in lib.view_users():
        print(f"- {user.name} (Email: {user.email}), Max Borrow: {user.max_borrow}")

    # Borrow books
    loan1 = lib.borrow_book(user1.id, book1.id)
    print(f"\n{user1.name} borrowed '{book1.title}' on {loan1.borrow_date.date()}, due on {loan1.due_date.date()}")

    loan2 = lib.borrow_book(user2.id, book2.id)
    print(f"{user2.name} borrowed '{book2.title}' on {loan2.borrow_date.date()}, due on {loan2.due_date.date()}")


    # search books
    print("\nSearch for books with 'the' in title:")
    results = lib.search_books(predicate=[title_contains("the")])
    for book in results:
        print(f"- {book.title} ({book.year})")


    print("Active loans for Alice:")
    results = lib.active_loans_for_user(user1.id)
    for loan in results:
        print(f"- {loan.book.title} (Due: {loan.due_date.date()})")

    # Return one book
    lib.return_book(loan1.id)
    print(f"\n{user1.name} returned '{book1.title}'")

    # search title substring
    print("\nSearch for books with 'the' in title:")
    results = lib.search_books(predicate=[title_contains("the")])
    for book in results:
        print(f"- {book.title} ({book.year})")

    # user active loans
    print("Active loans for Alice:")
    results = lib.active_loans_for_user(user1.id)
    for loan in results:
        print(f"- {loan.book.title} (Due: {loan.due_date.date()})")

if __name__ == "__main__":
    demo()