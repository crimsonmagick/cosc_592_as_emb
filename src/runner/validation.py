from subprocess import CompletedProcess


def validate_response(res: CompletedProcess):
    if res.returncode != 0:
        error = res.stderr.decode().replace("\n", ";")
        raise RuntimeError(f"{res.args[0]} returned code {res.returncode}, error={error}")
