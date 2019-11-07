import base64
import errno
import os


def store_image(directory='default', photo_name=None, image64=None):
    if photo_name is None or image64 is None:
        raise Exception('nome da foto ou imagem64 está None')

    imgdata = base64.b64decode(image64)

    path = '%s/%s.png' % (directory, photo_name)

    filename = 'imagens/%s' % path

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'wb') as f:
        f.write(imgdata)

    return path
