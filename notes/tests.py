from json import loads, dumps
from uuid import UUID, uuid4
from namegenerator import gen as random_name
from random import randint
from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import localtime, now

from .services import business_logic
from .models import Note


class NotesBusinessLogicTest(TestCase):
    def test_empty_array_of_notes(self):
        """
        When starting the program, an empty array should be returned
        """
        expected_result = []
        result = business_logic.listNotes()
        self.assertListEqual(expected_result, result)

    def test_array_of_2_notes(self):
        expected_result = [
            {'title': 'Mi genial nota', 'author': 'Amaury Pruebas',
                'body': 'Unit testing'},
            {'title': 'Mi genial nota 2', 'author': 'Amaury Pruebas 2',
                'body': 'Unit testing x2'}
        ]
        for note in expected_result:
            inserted_note = business_logic.createNote(
                title=note['title'], author=note['author'], body=note['body']
            )
            self.assertEqual(note['title'], inserted_note['title'])
            self.assertEqual(note['author'], inserted_note['author'])
            self.assertEqual(note['body'], inserted_note['body'])
            self.assertTrue(now() > inserted_note['created_at'])
        result = business_logic.listNotes()
        self.assertEqual(len(expected_result), len(result))

    def test_creation_of_note(self):
        """
        Creating a note with all the normal parameters
        """
        expected_result = {
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas',
            'body': 'Unit testing', 'created_at': now()
        }
        result = business_logic.createNote(
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
        result = business_logic.createNote(
            title=note_to_insert['title'], author=note_to_insert['author'], body=note_to_insert['body']
        )
        business_logic.deleteNote(result['uuid'])
        self.assertListEqual(business_logic.listNotes(), [])
        with self.assertRaises(Note.DoesNotExist):
            business_logic.getNote(result['uuid'])
        with self.assertRaises(Note.DoesNotExist):
            business_logic.deleteNote(result['uuid'])

    def test_get_inserted_note_after_inserting_5_notes(self):
        note_to_insert = {
            'title': 'Mi genial nota', 'author': 'Amaury Pruebas', 'body': 'Unit testing'
        }
        for i in range(5):
            business_logic.createNote(
                title=random_name(), author=random_name(), body=random_name()
            )
        random_note_to_get = business_logic.listNotes()[randint(0, 4)]
        result = business_logic.getNote(random_note_to_get['uuid'])
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

        expected_body = sent_body
        expected_status_code = 200
        expected_header = 'application/json'

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

    def test_get_inserted_note(self):
        created_note = business_logic.createNote(
            title='super titulo', author='Amaury Ortega', body='Amaury Ortega'
        )
        expected_note = {
            'title': created_note['title'],
            'body': created_note['body'],
            'author': created_note['author'],
            'uuid': str(created_note['uuid'])
        }
        expected_status_code = 200
        expected_header = 'application/json'

        response = self.client.get(
            reverse('notes.index') + str(created_note['uuid'])
        )
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertEqual(expected_note['title'], response.json()['title'])
        self.assertEqual(expected_note['body'], response.json()['body'])
        self.assertEqual(expected_note['author'], response.json()['author'])
        self.assertGreaterEqual(
            now(),
            datetime.strptime(
                response.json()['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
        )
        self.assertIsInstance(UUID(response.json()['uuid']), UUID)

    def test_delete_note(self):
        created_note = business_logic.createNote(
            title='super titulo', author='Amaury Ortega', body='Amaury Ortega'
        )
        expected_status_code = 200
        expected_header = 'application/json'
        expected_body = {
            'message': f"Note with UUID: {str(created_note['uuid'])} has been deleted"
        }
        response = self.client.delete(
            reverse('notes.index') + str(created_note['uuid'])
        )
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())
    
    def test_delete_non_existent_note(self):
        expected_status_code = 404
        expected_header = 'application/json'
        random_uuid = str(uuid4())
        expected_body = {
            'message': 'No note was found with UUID: ' + random_uuid
        }
        response = self.client.delete(
            reverse('notes.index') + random_uuid
        )
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

    def test_delete_endpoint_without_uuid(self):
        expected_status_code = 400
        expected_header = 'application/json'
        expected_body = {
            'message': 'Provide the UUID of the note that wants to be deleted'
        }
        response = self.client.delete(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

    def test_get_endpoint_with_non_existent_uuid(self):
        expected_status_code = 404
        expected_header = 'application/json'
        random_uuid = str(uuid4())
        expected_body = {
            'message': 'No note was found with UUID: ' + random_uuid
        }
        response = self.client.get(reverse('notes.index') + random_uuid)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

    def test_non_supported_http_method(self):
        expected_status_code = 405
        expected_header = 'application/json'
        expected_body = {
            'message': "Use one of the accepted HTTP methods ['GET', 'POST', 'DELETE']"
        }
        response = self.client.patch(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

        response = self.client.put(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

        response = self.client.options(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

        response = self.client.trace(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
        self.assertDictEqual(expected_body, response.json())

        response = self.client.head(reverse('notes.index'))
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response['Content-Type'], expected_header)
