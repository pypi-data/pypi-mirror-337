import chz

from loss_e.cli import decode_lse_file

@chz.chz
class Options:
    input: str = chz.field(doc="path to input file")


def main(opts: Options):
    with open(opts.input, "rb") as f:
        input_data = f.read()

    metadata, data = decode_lse_file(input_data)
    print("===")
    print(metadata)
    print("---")
    print(data)
    print("===")


if __name__ == "__main__":
    chz.nested_entrypoint(main)
