
def extract_route(request):
    return request.split('\n')[0].split(' ')[1][1:]


def read_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()


def load_data(name_file):
    import json
    with open(f'data/{name_file}') as f:
        data = json.load(f)
    return data


def load_template(name_file):
    with open(f'templates/{name_file}') as f:
        template = f.read()
    return template


def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += headers + '\n'
    response += '\n' + body

    return response.encode()
