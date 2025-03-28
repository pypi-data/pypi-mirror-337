import base64
import io
from typing import Any

from PIL import Image
from PIL.Image import Image as ImageType

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsVerticalImageValidator(BaseValidator):
    def __init__(self, error_message=None):
        self.error_message = (
            error_message or "The image is not vertically oriented."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, (str, ImageType)):
            raise ValidationError(
                "The value is not an image or its base 64 representation."
            )

        try:
            if isinstance(value, str):
                value = Image.open(io.BytesIO(base64.b64decode(value)))

            if value.width > value.height:
                raise

        except Exception:
            raise ValidationError(self.error_message)
