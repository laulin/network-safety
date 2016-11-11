import yaml
import sys

from tcpdump import Tcpdump

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

        tcpdump = Tcpdump(**configuration["capture"])
        process = tcpdump.popen()
        process.wait()
