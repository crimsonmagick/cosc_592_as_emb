import subprocess

from runner.validation import validate_response


def disassemble(source_path, *, strip: bool) -> str:
    if strip:
        validate_response(subprocess.run(["strip", source_path], capture_output=True))
    res = subprocess.run(["objdump", "--no-addresses", "--no-show-raw-insn", "-M intel", "-d", source_path],
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

