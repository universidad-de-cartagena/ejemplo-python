from json import loads
from uuid import UUID

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import localtime, now

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
        expected_result = [
            {'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing'},
            {'title': 'Mi genial nota 2', 'author': 'Amaury Pruebas 2', 'body': 'Unit testing x2'}
        ]
        for note in expected_result:
            inserted_note = bussiness_logic.createNote(title=note['title'], author=note['author'], body=note['body'])
            self.assertEqual(note['title'], inserted_note['title'])
            self.assertEqual(note['author'], inserted_note['author'])
            self.assertEqual(note['body'], inserted_note['body'])
            self.assertTrue(now() > inserted_note['created_at'])
        result = bussiness_logic.listNotes()
        self.assertEqual(len(expected_result), len(result))

    def test_creation_of_note(self):
        """
        Creating a note with all the normal parameters
        """
        expected_result = {'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing', 'created_at': now()}
        result = bussiness_logic.createNote(
            title=expected_result['title'], author=expected_result['author'], body=expected_result['body']
        )
        self.assertEqual(expected_result['title'], result['title'])
        self.assertEqual(expected_result['author'], result['author'])
        self.assertEqual(expected_result['body'], result['body'])
        self.assertTrue(expected_result['created_at'] < result['created_at'])
        self.assertIsInstance(result['uuid'], UUID)

    def test_delete_note(self):
        inserted_note = {'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing', 'created_at': now()}
        self.assertListEqual(bussiness_logic.listNotes(), [])
        result = bussiness_logic.createNote(
            title=inserted_note['title'], author=inserted_note['author'], body=inserted_note['body']
        )
        self.assertEqual(len(bussiness_logic.listNotes()), 1)
        bussiness_logic.deleteNote(result['uuid'])
        self.assertListEqual(bussiness_logic.listNotes(), [])

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
