import io
import os
import re
from typing import Literal
import base64
import sys
import zlib
import struct
import json

import filetype
import chz
from openai import OpenAI
import urllib

SUPPORTED_IMAGE_INPUT_TYPES = ["image/jpeg", "image/png"]
# MODEL = "gpt-4o-mini-2024-07-18"
MODEL = "gpt-4o-2024-08-06"
FILE_SIGNATURE = b"LOSS-E"


def decode_lse_file(input_data: bytes) -> tuple[dict, str]:
    f = io.BytesIO(input_data)
    signature = f.read(len(FILE_SIGNATURE))
    assert signature == FILE_SIGNATURE
    metadata_len = int.from_bytes(f.read(4), byteorder="little")
    metadata = json.loads(f.read(metadata_len).decode("utf8"))
    compressed_data = f.read()
    data = zlib.decompress(compressed_data).decode("utf8")
    return metadata, data


def encode_lse_file(metadata: dict, data: str) -> bytes:
    json_metadata = json.dumps(metadata)
    return (
        FILE_SIGNATURE
        + len(json_metadata).to_bytes(4, byteorder="little")
        + json_metadata.encode("utf8")
        + zlib.compress(data.encode("utf8"))
    )


def get_image_size(image_data: bytes, mime_type: str) -> tuple[int, int]:
    # based on https://stackoverflow.com/questions/8032642/how-can-i-obtain-the-image-size-using-a-standard-python-class-without-using-an
    if mime_type == "image/jpeg":
        pos = 0
        size = 2
        ftype = 0
        while not 0xC0 <= ftype <= 0xCF:
            pos += size
            byte = image_data[pos]
            pos += 1
            while byte == 0xFF:
                byte = image_data[pos]
                pos += 1
            ftype = byte
            size = struct.unpack(">H", image_data[pos : pos + 2])[0] - 2
            pos += 2
        # We are at a SOFn block
        pos += 1  # Skip `precision" byte.
        height, width = struct.unpack(">HH", image_data[pos : pos + 4])
        return width, height
    elif mime_type == "image/png":
        check = struct.unpack(">i", image_data[4:8])[0]
        if check == 0x0D0A1A0A:
            return struct.unpack(">ii", image_data[16:24])
    raise Exception(f"Unsupported image type {mime_type}")


def compress_image(client: OpenAI, input_data: bytes, mime_type: str) -> bytes:
    base64_image = base64.b64encode(input_data).decode("utf8")
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please describe this image in excruciating detail:",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}",
                        "detail": "high",
                    },
                },
            ],
        }
    ]
    request = dict(
        model=MODEL,
        messages=messages,
        seed=0,
    )
    completion = client.chat.completions.create(**request)
    description = completion.choices[0].message.content
    width, height = get_image_size(input_data, mime_type)
    return encode_lse_file(dict(type="image", width=width, height=height), description)


def decompress_image(client: OpenAI, description: str) -> bytes:
    # https://platform.openai.com/docs/guides/image-generation
    response = client.images.generate(
        model="dall-e-3",
        prompt="I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:\n"
        + description,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    resp = urllib.request.urlopen(response.data[0].url)
    output_data = resp.read()
    return output_data


def compress_text(client: OpenAI, input_data: str) -> bytes:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Summarize the following novel in intricate detail with an outline of the contents of the novel.  Each bullet point in the outline should be numbered such as 1), 2), ... etc..",
                },
                {"type": "text", "text": input_data},
            ],
        }
    ]
    request = dict(
        model=MODEL,
        messages=messages,
        seed=0,
    )
    completion = client.chat.completions.create(**request)
    outline = completion.choices[0].message.content
    return encode_lse_file(dict(type="text", word_count=len(input_data.split())), outline)


def decompress_text(client: OpenAI, metadata: dict, outline: str) -> str:
    m = re.findall(r"(\d+)\) ", outline)
    section_count = max(int(r) for r in m)
    result = ""
    for section in range(section_count):
        prompt = ""
        if section == 0:
            prompt += f"Here is the outline for a novel. "
        prompt = f"please write out a full length section of the novel for section {section}) of the outline. DO NOT skip or omit any parts, and make sure you generate at least {metadata['word_count']/section_count} words.  You should generate the full section and not prompt me with any questions.\n\n"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {"type": "text", "text": outline},
                ],
            }
        ]
        request = dict(
            model=MODEL,
            messages=messages,
            seed=0,
        )
        completion = client.chat.completions.create(**request)
        content = completion.choices[0].message.content
        result += content + "\n\n"
    return result.encode("utf8")

@chz.chz
class Options:
    mode: Literal["compress", "decompress"]
    input: str = chz.field(doc="path to input file")
    output: str = chz.field(doc="path to output file")
    debug: bool = False


def cli(opts: Options):
    if not os.path.exists(opts.input):
        print(f"input file {opts.input} not found")
        sys.exit(1)

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    if opts.mode == "compress":
        kind = filetype.guess(opts.input)
        with open(opts.input, "rb") as f:
            input_data = f.read()
        if kind is None:
            # assume text
            output_data = compress_text(client, input_data.decode("utf8"))
        else:
            if kind.mime not in SUPPORTED_IMAGE_INPUT_TYPES:
                print(
                    f"input file {opts.input} not a supported image type, only {', '.join(SUPPORTED_IMAGE_INPUT_TYPES)} are supported"
                )
                sys.exit(1)
            output_data = compress_image(client, input_data, kind.mime)

        with open(opts.output, "wb") as f:
            f.write(output_data)

        if opts.debug:
            with open(opts.output, "rb") as f:
                metadata, data = decode_lse_file(f.read())
            print("===")
            print(metadata)
            print("---")
            print(data)
            print("===")

        input_size_bytes = os.path.getsize(opts.input)
        output_size_bytes = os.path.getsize(opts.output)
        compression = output_size_bytes / input_size_bytes
        if compression <= 1:
            ratio = f"{int(round(input_size_bytes / output_size_bytes))}:1"
        else:
            ratio = f"1:{int(round(output_size_bytes / input_size_bytes))}"

        print(
            f"Compressed {opts.input} ({input_size_bytes} bytes) => {opts.output} ({output_size_bytes} bytes), compression ratio {ratio}"
        )
    else:
        assert opts.mode == "decompress"
        with open(opts.input, "rb") as f:
            input_data = f.read()
        metadata, data = decode_lse_file(input_data)
        if metadata["type"] == "text":
            output_data = decompress_text(client, metadata, data)
        elif metadata["type"] == "image":
            output_data = decompress_image(client, data)
        else:
            raise Exception(f"Invalid type {metadata['type']}")
        
        with open(opts.output, "wb") as f:
            f.write(output_data)


def main():
    chz.nested_entrypoint(cli)


if __name__ == "__main__":
    main()
