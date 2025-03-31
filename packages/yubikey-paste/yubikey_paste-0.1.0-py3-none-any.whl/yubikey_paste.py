import yubikey_manager_lib
import subprocess
import tomllib
import os.path


def main():
    with open(os.path.expanduser("~/.config/yubikey-paste/config.toml"), "rb") as f:
        config = tomllib.load(f)
    pasted = subprocess.check_output(["wl-paste", "--primary"], encoding="utf8")[:-1]
    slot = config["mappings"][pasted]
    ykman = yubikey_manager_lib.YKMan()
    value = ykman.run("oath", "accounts", "code", "-s", slot)["stdout"][0]
    subprocess.check_call(
        [
            "sudo",
            "/usr/bin/injectinput",
            value + "\\r"
        ]
    )
