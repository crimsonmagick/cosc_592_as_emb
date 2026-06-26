import subprocess

from src.runner.validation import validate_response


def disassemble(object_file, *, strip: bool) -> str:
    """Disassembles an object file at a given path.

    :param object_file: relocatable binary object to disassemble. COFF and ELF formats supported
    :param strip: Strips the object file of its symbols if set to True
    :return: Assembly code as a String
    """
    if strip:
        validate_response(subprocess.run(["strip", object_file], capture_output=True))
    res = subprocess.run(["objdump", "--no-addresses", "--no-show-raw-insn", "-M intel", "-d", object_file],
                         capture_output=True)
    validate_response(res)
    raw_output_lines = res.stdout.decode().split('\n')
    idx = 0
    # assumes we'll always have .text in the diassembly
    for idx, line in enumerate(raw_output_lines):
        if '.text' in line:
            break
    normalized_output = '\n'.join(raw_output_lines[idx + 1:])
    return normalized_output

