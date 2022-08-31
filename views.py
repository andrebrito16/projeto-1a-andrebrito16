from urllib import request, parse
from utils import load_template, build_response
from database.database import Database, Note
from database.instance import DatabaseInstance


def index(request, db):
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    code = 200
    reason = 'OK'
    headers = ''
    if request.split(' ')[1].startswith('/delete'):
        code = 303
        reason = 'See Other'
        headers = 'Location: /'

    if request.startswith('POST') and not request.split(' ')[1].startswith('/edit'):
        print(request)
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        code = 303
        reason = 'See Other'
        headers = 'Location: /'
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = parse.unquote_plus(valor)
        new_note = Note(None, params['titulo'], params['detalhes'])
        db.add(new_note)
    elif request.startswith('POST') and request.split(' ')[1].startswith('/edit'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        code = 303
        reason = 'See Other'
        headers = 'Location: /'
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = parse.unquote_plus(valor)
        note_id = request.split(' ')[1].split('/')[-1]
        edit_note = Note(note_id, params['titulo'], params['detalhes'])
        print(edit_note)
        db.update(edit_note)
        print(note_id)
    note_template = load_template('components/note.html')
    notes = db.get_all()

    notes_li = [
        note_template.format(
            id=dados.id, title=dados.title, details=dados.content)
        for dados in notes
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(body, code, reason, headers)
