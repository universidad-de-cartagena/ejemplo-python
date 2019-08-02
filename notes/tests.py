from json import loads, dumps
from uuid import UUID
from namegenerator import gen as random_name
from random import randint
from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import localtime, now

from .services import bussiness_logic
from .models import Note


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
            {'title': 'Mi genial nota', 'author': 'Amaury Pruebas',
                'body': 'Unit testing'},
            {'title': 'Mi genial nota 2', 'author': 'Amaury Pruebas 2',
                'body': 'Unit testing x2'}
        ]
        for note in expected_result:
            inserted_note = bussiness_logic.createNote(
                title=note['title'], author=note['author'], body=note['body']
            )
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
        expected_result = {
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas',
            'body': 'Unit testing', 'created_at': now()
        }
        result = bussiness_logic.createNote(
            title=expected_result['title'], author=expected_result['author'], body=expected_result['body']
        )
        self.assertEqual(expected_result['title'], result['title'])
        self.assertEqual(expected_result['author'], result['author'])
        self.assertEqual(expected_result['body'], result['body'])
        self.assertLessEqual(
            expected_result['created_at'], result['created_at'])
        self.assertIsInstance(result['uuid'], UUID)

    def test_delete_note(self):
        note_to_insert = {
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing'
        }
        result = bussiness_logic.createNote(
            title=note_to_insert['title'], author=note_to_insert['author'], body=note_to_insert['body']
        )
        bussiness_logic.deleteNote(result['uuid'])
        self.assertListEqual(bussiness_logic.listNotes(), [])
        with self.assertRaises(Note.DoesNotExist):
            bussiness_logic.getNote(result['uuid'])
            bussiness_logic.deleteNote(result['uuid'])

    def test_get_inserted_note_after_inserting_5_notes(self):
        random_name()
        note_to_insert = {
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing'
        }
        for i in range(5):
            bussiness_logic.createNote(
                title=random_name(), author=random_name(), body=random_name()
            )
        random_note_to_get = bussiness_logic.listNotes()[randint(0, 4)]
        result = bussiness_logic.getNote(random_note_to_get['uuid'])
        self.assertIsNotNone(result)
        self.assertIsInstance(result['uuid'], UUID)
        self.assertIsInstance(result['title'], str)
        self.assertIsInstance(result['author'], str)
        self.assertIsInstance(result['body'], str)
        self.assertIsInstance(result['created_at'], datetime)


class NotesIntegrationTest(TestCase):
    def test_empty_array_of_notes(self):
        """
        When starting the program, an empty JSON array must be returned
        """
        expected_body = []
        expected_header = 'application/json'
        expected_status_code = 200

        response = self.client.get(reverse('notes.index'))

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertListEqual(response.json(), expected_body)

    def test_insert_note(self):
        sent_body = {
            'title': 'super titulo',
            'body': 'super mega contenido raro',
            'author': 'Amaury Ortega'
        }
        sent_header = 'application/json'

        expected_body = sent_body
        expected_status_code = 200
        expected_header = sent_header

        response = self.client.post(
            reverse('notes.index'), dumps(sent_body), 'application/json'
        )
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertEqual(sent_body['title'], response.json()['title'])
        self.assertEqual(sent_body['body'], response.json()['body'])
        self.assertEqual(sent_body['author'], response.json()['author'])
        self.assertGreaterEqual(
            now(),
            datetime.strptime(
                response.json()['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
        )
        self.assertIsInstance(UUID(response.json()['uuid']), UUID)

