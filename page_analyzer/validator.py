from validators import url


def validate(data):
    errors = {}
    if url(data['url']) and len(data['url']) <= 255:
        return False
    if len(data['url']) > 255:
        errors['name'] = 'URL превышает 255 символов'
    if not url(data['url']):
        errors['name'] = 'Некорректный URL'
    return errors
