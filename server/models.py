from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import List, Optional
import uuid

class Writes(SQLModel, table=True):
    isbn: str = Field(foreign_key="book.isbn", primary_key=True)
    author_id: int = Field(foreign_key="author.id", primary_key=True)

class Author(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    first_name: str = Field(nullable=False)
    middle_name_init: Optional[str] = Field(default=None)
    last_name: str = Field(nullable=False)

    books: List["Book"] = Relationship(back_populates="authors", link_model=Writes)

    __table_args__ = (UniqueConstraint('first_name', 'middle_name_init', 'last_name', name='uq_author_name'),)

class Publisher(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str = Field(unique=True, nullable=False)

    books: List["Book"] = Relationship(back_populates="publisher")

class Book(SQLModel, table=True):
    isbn: str = Field(primary_key=True, max_length=13, min_length=10, nullable=False)
    title: str = Field(nullable=False)
    qty: int = Field(nullable=False, default=1, ge=1)
    publisher_id: int = Field(foreign_key="publisher.id")

    authors: List["Author"] = Relationship(back_populates="books", link_model=Writes)
    publisher: "Publisher" = Relationship(back_populates="books")
    copies: List["Copy"] = Relationship(back_populates="book")

class Copy(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_isbn: str = Field(foreign_key="book.isbn", primary_key=True)
    barcode_path: str = Field(nullable=True)

    book: "Book" = Relationship(back_populates="copies")

class Patron(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    phone: str = Field(nullable=False, unique=True)
    barcode_path: str = Field(nullable=True)

class Library(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    timezone: str = Field(nullable=False)

class Librarian(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    hashed_pw: str = Field(nullable=False)
    is_admin: bool = Field(nullable=False)