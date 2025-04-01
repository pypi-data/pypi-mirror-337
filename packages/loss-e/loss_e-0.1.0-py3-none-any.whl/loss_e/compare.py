import os
import base64
import sys
import re

import filetype
import chz
from openai import OpenAI

from loss_e.cli import SUPPORTED_IMAGE_INPUT_TYPES

SUPPORTED_IMAGE_INPUT_TYPES = ["image/jpeg", "image/png"]
MODEL = "gpt-4o-mini-2024-07-18"


@chz.chz
class Options:
    first: str = chz.field(doc="path to first input file")
    second: str = chz.field(doc="path to second input file")
    debug: bool = True


def encode_image(filepath: str, mime_type: str) -> dict:
    with open(filepath, "rb") as f:
        input_data = f.read()
         
    base64_image = base64.b64encode(input_data).decode("utf8")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime_type};base64,{base64_image}",
            "detail": "high",
        },
    }


def main(opts: Options):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    image_filepaths = [opts.first, opts.second]
    kinds = []
    for image_filepath in image_filepaths:
        kind = filetype.guess(image_filepath)
        if kind.mime not in SUPPORTED_IMAGE_INPUT_TYPES:
            print(
                f"input file {opts.input} not a supported image type, only {", ".join(SUPPORTED_IMAGE_INPUT_TYPES)} are supported"
            )
            sys.exit(1)
        kinds.append(kind)
    
    images = [encode_image(image_filepath, kind.mime) for image_filepath, kind in zip(image_filepaths, kinds, strict=True)]
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Corporate needs you to find the difference between this picture and this picture.

Describe the differences between the two images.  Once you've done that, choose a number between 1 and 10, inclusive, representing how significant the differences are.  10 meaning that the images are identical, and 1 meaning that they are completely different images.  When you output the number, prefix it with "Answer:".""",
                },
            ] + images,
        }
    ]
    request = dict(
        model=MODEL,
        messages=messages,
        seed=0,
    )
    completion = client.chat.completions.create(**request)
    output = completion.choices[0].message.content
    if opts.debug:
        print("===")
        print(output)
        print("===")
        
    m = re.search(r"Answer:\s*(\d+)", output)
    if m is None:
        print("Failed to find score in prompt")
    else:
        score = int(m.groups()[0])
        print(f"Corporate similarity: {score}")


if __name__ == "__main__":
    chz.nested_entrypoint(main)
