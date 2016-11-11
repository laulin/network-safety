import logging
import subprocess

class Tshark:
    def __init__(self, fields):
        self._fields = fields

    def make_command(self, input_filename):
        cmd = ["tshark",
                "-r", input_filename,
                "-T", "fields"]

        for field in self._fields:
            cmd += ["-e", field]

        cmd += ["-E", "header=y", "-E", "separator=,", "-E", "quote=d"]

        return cmd

    def check_output(self, input_filename):
        cmd = self.make_command(input_filename)
        output = subprocess.check_output(cmd)
        output = output.decode("utf8")
        return output

if __name__ == "__main__":
    import sys
    tshark = Tshark(["frame.len", "frame.time_epoch", "eth.src", "eth.dst", "ip.src", "ip.dst"])
    output = tshark.check_output(sys.argv[1])

    print(output)
