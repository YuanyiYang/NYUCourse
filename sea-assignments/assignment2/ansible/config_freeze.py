import subprocess
import json

if __name__ == "__main__":
    proc = subprocess.Popen("hostfiles/ec2.py", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    hosts = json.loads(out)["_meta"]["hostvars"]
    config = {"backends": [hosts[key]["ec2_private_ip_address"] for key in hosts.keys() \
                if hosts[key]["ec2_tag_Role"] == "backend"]}

    f = open("config.json", "w")
    f.write(json.dumps(config))
    f.close()

  # In your frontend, read this config file like this:
  # BACKENDS = json.load(open("config.json", "r"))["backends"]
