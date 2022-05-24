from __future__ import annotations
import random
import string
import functools
from typing import TYPE_CHECKING
# import blog_app.models as _models

def generate__code(limit, prefix, model):
    characters = string.ascii_letters + string.digits + string.punctuation
    flag_check = True
    _code = None
    display_code = None
    _code_list = model.objects.values_list("post_code", flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=limit))
        display_code = f"#{prefix}{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code

def _post_code():
    import blog_app.models as _models
    return functools.partial(generate__code, limit=10, prefix="POST", model=_models.Post)

generate__post_code = _post_code()

generate__image_code = functools.partial(generate__code, limit=8, prefix="IMAGE", model=_models.Image)
generate__comment_code = functools.partial(generate__code, limit=10, prefix="COMMENT", model=_models.Comment)

if __name__ == "__main__":
    pass