from validators import url


def validate(data):
    errors = {}
    if url(data['url']) == True and len(data['url']) <= 255:
        return False
    if len(data['url']) > 255:
        errors['name'] = 'URL превышает 255 символов'
    if url(data['url']) != True:
        errors['name'] = 'Некорректный URL'
    return errors
