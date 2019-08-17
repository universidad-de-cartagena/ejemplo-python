from json import loads
from uuid import UUID, uuid4

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .services import createNote, deleteNote, getNote, listNotes
from .models import Note

json_dumps_params = {'sort_keys': True, 'indent': 2}
accepted_http_methods = ['GET', 'POST', 'DELETE']


def index(request: HttpRequest, note_uuid: UUID = None):
    def error_message(message: str, http_code: int = 400) -> JsonResponse:
        """
        Helper error message function
            :param message:str: Message sent in the response.
            :param http_code:int: Status code in the response, by default is ```400```.
            :return: HttpResponse with error message and status code
            :rtype: django.http.JsonResponse
        """
        _error_message = {'message': message}
        return JsonResponse(_error_message, json_dumps_params=json_dumps_params, status=http_code)

    if request.method not in accepted_http_methods:
        return error_message(f'Use one of the accepted HTTP methods {accepted_http_methods}', http_code=405)

    elif request.method == 'GET':
        if note_uuid is not None:
            try:
                response = getNote(note_uuid)
            except Note.DoesNotExist as ex:
                return error_message(f'No note was found with UUID: {str(note_uuid)}', 404)
            return JsonResponse(response, json_dumps_params=json_dumps_params)
        response = listNotes()
        return JsonResponse(response, json_dumps_params=json_dumps_params, safe=False)

    elif request.method == 'POST':
        body = loads(request.body.decode('utf-8'))
        response = createNote(title=body['title'], author=body['author'], body=body['body'])
        return JsonResponse(response, json_dumps_params=json_dumps_params)

    elif request.method == 'DELETE':
        if note_uuid is None:
            return error_message('Provide the UUID of the note that wants to be deleted', 400)
        try:
            deleteNote(note_uuid)
        except Note.DoesNotExist as ex:
            return error_message(f'No note was found with UUID: {str(note_uuid)}', 404)
        response = { 'message': f'Note with UUID: {str(note_uuid)} has been deleted' }
        return JsonResponse(response, json_dumps_params=json_dumps_params)
