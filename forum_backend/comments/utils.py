import secrets

def part_file(filename):
    return filename.split('.')


def images_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'images/{new_name}.{extension}'


def videos_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'videos/{new_name}.{extension}'


def files_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'files/{new_name}.{extension}'
