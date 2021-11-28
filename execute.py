import subprocess


def command(c, directory=None) -> tuple:
    c = c.split()
    # Executing the command
    if directory:
        process = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=directory)
    else:
        process = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")
    return stdout, stderr
