from validators import url


def validate(url_name):
    errors = {}
    if url(url_name) and len(url_name) <= 255:
        return errors
    if len(url_name) > 255:
        errors['name'] = 'URL превышает 255 символов'
    if not url(url_name):
        errors['name'] = 'Некорректный URL'
    return errors
