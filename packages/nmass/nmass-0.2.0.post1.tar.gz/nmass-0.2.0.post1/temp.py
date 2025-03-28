from nmass.masscan import Masscan
from nmass.nmap import Nmap

if __name__ == "__main__":
    masscan = Masscan().with_targets("135.224.95.165/24").with_ports(21).with_rate(10000)
    nmap = Nmap().with_step(masscan.run()).without_ping().with_scripts("ftp-anon")

    if result := nmap.run():
        with open("result.txt", "w") as f:
            n = f.write(result.model_dump_json(exclude_none=True))
            print(f"Write {n} chars to result.txt")
