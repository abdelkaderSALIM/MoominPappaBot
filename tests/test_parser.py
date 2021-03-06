"""This module test the parser class."""

from src.parser import Parser


class TestParser:
    PARSER = Parser()

    # TEST UNITAIRE

    def test_remove_case_sensitive(self):
        assert (
            self.PARSER.remove_case_sensitive("Emmène-moi à Moomin World ?")
            == "emmène-moi à moomin world ?"
        )

    def test_remove_accents(self):
        assert (
            self.PARSER.remove_accents("Emmène-moi à Moomin World ?")
            == "Emmene-moi a Moomin World ?"
        )

    def test_remove_ponctuation(self):
        assert (
            self.PARSER.remove_ponctuation(
                "Bonjour, emmène-moi à Moomin World ?"
            )
            == "Bonjour emmène moi à Moomin World"
        )

    def test_remove_stop_words(self):
        assert (
            self.PARSER.remove_stop_words("aux Pays des Moomins")
            == "Pays Moomins"
        )

    # TEST D'INTEGRATION

    def test_process_question(self):
        sentence = "Où est Moomin World ? Hein? Alors, je t'écoute !"
        assert self.PARSER.process_question(sentence) == "moomin world tecoute"
