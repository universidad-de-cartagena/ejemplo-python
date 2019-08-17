from django.db.models import QuerySet
from django.utils.timezone import localtime, now

from ..models import Note


def listNotes() -> list:
    """
    List all the notes in the database. Returns a Python list with notes.
    Note: {
        'uuid': obj uuid.UUID, 'title': str, 'author': str,
        'body': str, 'created_at': obj datetime.datetime
    }
    """
    list_of_notes = []
    for note in Note.objects.all():
        list_of_notes.append({
            'uuid': note.uuid, 'title': note.title,
            'author': note.author, 'body': note.body, 'created_at': localtime(note.created_at)
        })
    return list_of_notes


def getNote(note_uuid) -> dict:
    """
    Gets a note based on a uuid.UUID, if the note doesn't exist, Note.DoesNotExist exception is raised.
    Note: {
        'uuid': obj uuid.UUID, 'title': str, 'author': str,
        'body': str, 'created_at': obj datetime.datetime
    }
    """
    try:
        found_note = Note.objects.get(uuid=note_uuid)
    except Note.DoesNotExist as e:
        message = f'getNote could not find a note with uuid: {str(note_uuid)}'
        raise Note.DoesNotExist(message) from e
    return {
        'uuid': found_note.uuid, 'title': found_note.title,
        'author': found_note.author, 'body': found_note.body, 'created_at': localtime(found_note.created_at)
    }


def createNote(title, author, body) -> dict:
    """
    Creates a note in the database and responds with its content.
    Note: {
        'uuid': obj uuid.UUID, 'title': str, 'author': str,
        'body': str, 'created_at': obj datetime.datetime
    }
    """
    new_note = Note(title=title, author=author, body=body, created_at=now())
    new_note.save()
    return {
        'uuid': new_note.uuid, 'title': new_note.title,
        'author': new_note.author, 'body': new_note.body, 'created_at': localtime(new_note.created_at)
    }


def deleteNote(note_uuid):
    """
    Deletes a note based on uuid.UUID, if the note to delete does not exists,
    a Note.DoesNotExist exception is raised. If the note is deleted, no response is given
    """
    try:
        found_note = Note.objects.get(uuid=note_uuid)
    except Note.DoesNotExist as e:
        message = f'deleteNote could not delete the note because getNote could not find a note with uuid: {str(note_uuid)}'
        raise Note.DoesNotExist(message) from e
    Note.objects.filter(uuid=found_note.uuid).delete()
