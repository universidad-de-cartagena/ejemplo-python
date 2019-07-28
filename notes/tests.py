from json import loads

from django.test import Client, TestCase
from django.urls import reverse

from .services import bussiness_logic


class NotesBussinessLogicTest(TestCase):
    def test_empty_array_of_notes(self):
        """
        When starting the program, an empty array should be returned
        """
        expected_result = []
        result = bussiness_logic.listNotes()
        self.assertListEqual(expected_result, result)

    def test_array_of_2_notes(self):
        """
        When starting the program, an empty array should be returned
        """
        expected_result = []
        expected_result.append({
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing'
        })
        expected_result.append({
            'title': 'Mi genial nota 2', 'author': 'Amaury Pruebas 2', 'body': 'Unit testing x2'
        })
        result = bussiness_logic.listNotes()
        self.assertListEqual(expected_result, result)

    def test_creation_of_note(self):
        """
        Creating a note with all the normal parameters
        """
        pass


class NotesIntegrationTest(TestCase):
    def test_empty_array_of_notes(self):
        """
        When starting the program, an empty JSON should be returned
        """
        expected_body = ["name"]
        expected_header = 'application/json'
        expected_status_code = 200

        response = self.client.get(reverse('notes.index'))

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertListEqual(loads(response.content), expected_body)
