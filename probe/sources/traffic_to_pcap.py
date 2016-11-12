import yaml
import sys
import logging.config

from tcpdump import Tcpdump

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

    logging.config.dictConfig(configuration["logging"])

    c = configuration["capture"]
    tcpdump = Tcpdump(c["interface"], c["buffer_size"], c["pcap_size"], c["pcap_timeout"], c["output_filename"], c["user"])
    process = tcpdump.popen()
    process.wait()
