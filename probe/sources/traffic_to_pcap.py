import yaml
import sys

from tcpdump import Tcpdump

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

    c = configuration["capture"]
    tcpdump = Tcpdump(c["interface"], c["buffer_size"], c["pcap_size"], c["pcap_timeout"], c["output_filename"])
    process = tcpdump.popen()
    process.wait()
