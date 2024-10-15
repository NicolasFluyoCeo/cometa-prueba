from typing import List, Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    description: Optional[str] = None
    contributor: str
    author: str
    contributor_note: Optional[str] = None
    price: float
    age_group: Optional[str] = None
    publisher: str
    primary_isbn13: str
    primary_isbn10: str


class ReviewSchema(BaseModel):
    book_review_link: Optional[str] = None
    first_chapter_link: Optional[str] = None
    sunday_review_link: Optional[str] = None
    article_chapter_link: Optional[str] = None


class ISBNSchema(BaseModel):
    isbn10: str
    isbn13: str


class BookResultSchema(BaseModel):
    list_name: str
    display_name: str
    bestsellers_date: str
    published_date: str
    rank: int
    rank_last_week: int
    weeks_on_list: int
    asterisk: int
    dagger: int
    amazon_product_url: str
    isbns: List[ISBNSchema]
    book_details: List[BookSchema]
    reviews: List[ReviewSchema]


class BookListSchema(BaseModel):
    num_results: int
    results: List[BookResultSchema]
    page_size: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.page_size = len(self.results) if isinstance(self.results, List) else 0


class BooksSearchCriteriaSchema(BaseModel):
    list: Optional[str] = None
    bestsellers_date: Optional[str] = None
    published_date: Optional[str] = None
    offset: Optional[int] = 0


class BookGenreSchema(BaseModel):
    code: str
    display_name: str
