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
        try:
            output = subprocess.check_output(cmd)
            output = output.decode("utf8")
            return output
        except:
            process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            process.wait()
            out, err = process.communicate()
            errcode = process.returncode
            raise Exception("process tshark finished with {} recturn code : stdout : '{}' stderr : '{}'".format(errcode, out.decode("utf8"), err.decode("utf8")))

if __name__ == "__main__":
    import sys
    tshark = Tshark(["frame.len", "frame.time_epoch", "eth.src", "eth.dst", "ip.src", "ip.dst"])
    output = tshark.check_output(sys.argv[1])

    print(output)
