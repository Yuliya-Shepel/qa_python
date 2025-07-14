import unittest


class BooksCollector:
    def __init__(self):
        self.books_genre = {}
        self.adult_ratings = ["18+", "21+", "Рекомендуется для взрослых"]
        self.favorites = set()

    def add_new_book(self, name):
        self.books_genre[name] = None

    def set_book_genre(self, name, genre):
        if name not in self.books_genre:
            raise ValueError(f"Книга '{name}' не найдена.")
        self.books_genre[name] = genre

    def get_book_genre(self, name):
        return self.books_genre.get(name)

    def get_books_for_children(self):
        return [name for name, genre in self.books_genre.items() if genre is None]

    def add_book_with_rating(self, name, rating):
        self.books_genre[name] = rating

    def is_for_children(self, name):
        return self.get_book_genre(name) is None

    def get_books_genre(self, name):
        """Возвращает жанр книги или None, если не найдено."""
        return self.get_book_genre(name)

    def add_book_in_favorites(self, name):
        if name not in self.books_genre:
            raise ValueError(f"Книга '{name}' не найдена.")
        self.favorites.add(name)

    def delete_book_from_favorites(self, name):
        self.favorites.discard(name)

    def get_list_of_favorites_books(self):
        return list(self.favorites)


class TestBooksCollectorExtended(unittest.TestCase):

    def setUp(self):
        self.bc = BooksCollector()


    def test_get_books_genre_existing_and_nonexistent(self):
        book_name = "Тестовая книга"
        genre = "Фантастика"
        self.bc.add_new_book(book_name)
        self.bc.set_book_genre(book_name, genre)


        with self.subTest("Existing book"):
            result = self.bc.get_books_genre(book_name)
            self.assertEqual(result, genre)


        with self.subTest("Non-existent book"):
            result_none = self.bc.get_books_genre("Неизвестная книга")
            self.assertIsNone(result_none)


    def test_add_book_in_favorites_and_duplicate(self):
        book_name = "Любимая книга"
        self.bc.add_new_book(book_name)


        self.bc.add_book_in_favorites(book_name)
        favs = self.bc.get_list_of_favorites_books()

        with self.subTest("Add to favorites"):
            self.assertIn(book_name, favs)


        try:
            self.bc.add_book_in_favorites(book_name)
            success = True
        except Exception:
            success = False
        with self.subTest("Add duplicate to favorites"):
            self.assertTrue(success)


    def test_delete_book_from_favorites(self):
        book_name = "Удаляемая книга"
        self.bc.add_new_book(book_name)


        self.bc.add_book_in_favorites(book_name)


        self.bc.delete_book_from_favorites(book_name)

        favs = self.bc.get_list_of_favorites_books()

        with self.subTest("Book removed from favorites"):
            self.assertNotIn(book_name, favs)


    def test_get_list_of_favorites_books_multiple_entries(self):
        books = ["Книга 1", "Книга 2", "Книга 3"]

        for b in books:
            if b not in self.bc.books_genre:
                self.bc.add_new_book(b)
            try:
                self.bc.add_book_in_favorites(b)
            except Exception:
                pass

        favs = set(self.bc.get_list_of_favorites_books())

        with self.subTest("Favorites contain all added books"):
            for b in books:
                self.assertIn(b, favs)



if __name__ == "__main__":
    unittest.main()
