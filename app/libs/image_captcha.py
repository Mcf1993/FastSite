import base64
import hashlib
import random
import time
import string
from io import BytesIO

from app.core.redis import RedisCls
from captcha.image import ImageCaptcha


class ImageCaptchaCls:
    CAPTCHA_SECRET_KEY = 'y7JntUWjDUNDrH+BSeV57w=='

    def _get_random_str(self):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        m = hashlib.sha256()
        m.update(
            bytes(f'{random_str}-{int(time.time())}-{self.CAPTCHA_SECRET_KEY}', encoding='utf-8')
        )
        hash_key = m.hexdigest()
        return random_str, hash_key

    def _image_to_base64(self, image_io: BytesIO):
        image_base64 = base64.b64encode(image_io.read()).decode()
        return image_base64

    def generate_image(self):
        random_str, hash_key = self._get_random_str()
        redis_cls = RedisCls()
        redis_cls.set(hash_key, random_str, 300)
        image = ImageCaptcha(width=280, height=90)
        image_io = image.generate(random_str)
        return hash_key, self._image_to_base64(image_io)

