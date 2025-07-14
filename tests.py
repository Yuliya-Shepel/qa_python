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

    def test_add_new_book_and_check_absence_of_genre(self):
        book_name = "Детская книга"
        self.bc.add_new_book(book_name)
        self.assertIn(book_name, self.bc.books_genre)
        self.assertIsNone(self.bc.get_book_genre(book_name))
        self.assertIn(book_name, self.bc.get_books_for_children())

    def test_set_and_get_book_genre(self):
        book_name = "Книга с жанром"
        self.bc.add_new_book(book_name)
        genre = "Фантастика"
        self.bc.set_book_genre(book_name, genre)
        self.assertEqual(self.bc.get_book_genre(book_name), genre)

    def test_get_books_for_children_returns_only_books_without_genres(self):
        self.bc.add_new_book("Детская 1")
        self.bc.add_new_book("Детская 2")
        self.bc.add_new_book("Взрослая")
        self.bc.set_book_genre("Взрослая", "Роман")

        children_books = self.bc.get_books_for_children()

        self.assertIn("Детская 1", children_books)
        self.assertIn("Детская 2", children_books)
        self.assertNotIn("Взрослая", children_books)

    def test_add_book_with_rating_and_check_is_for_children(self):
        book_name = "Родительская книга"
        rating = "18+"
        self.bc.add_book_with_rating(book_name, rating)

        self.assertEqual(self.bc.get_book_genre(book_name), rating)
        self.assertFalse(self.bc.is_for_children(book_name))

    def test_is_for_children_returns_true_for_books_without_rating(self):
        book_name = "Детская книга"
        self.bc.add_new_book(book_name)

        self.assertTrue(self.bc.is_for_children(book_name))

    def test_set_book_genre_raises_error_for_unknown_book(self):
        with self.assertRaises(ValueError):
            self.bc.set_book_genre("Не существующая книга", "Фантастика")

    def test_get_book_genre_returns_none_for_unknown_book(self):
        result = self.bc.get_book_genre("Неизвестная книга")
        self.assertIsNone(result)

    def test_get_books_for_children_returns_empty_when_no_books_without_genres(self):
        bc2 = BooksCollector()
        bc2.add_new_book("Книга 1")
        bc2.set_book_genre("Книга 1", "Фантастика")
        bc2.add_new_book("Книга 2")
        bc2.set_book_genre("Книга 2", "Роман")

        result = bc2.get_books_for_children()
        self.assertEqual(result, [])

    def test_add_duplicate_book_does_not_raise_error_and_overwrites_if_needed(self):
        book_name = "Повторная книга"

        self.bc.add_new_book(book_name)

        try:
            self.bc.add_new_book(book_name)
            success = True
        except Exception:
            success = False

        self.assertTrue(success)

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
