#!/usr/bin/python3
"""
MIT LICENSE

The entry of known_hosts is composed of three parts and two separators(space): (hostname[s] or hashed hostname[s])<space>(ssh algo)<space>(public key)
ref: https://serverfault.com/questions/331080/what-do-the-different-parts-of-known-hosts-entries-mean

This script works on only basic assumption
- different hosts have different fingerprint with different signature algorithms and hash algorithms

So I assume ***that the entries having the same pubkey/fingerprint should be duplicate***, then I keep the latest one only.

usage:
    python known_hosts_dedup.py [known_hosts]=~/.ssh/known_hosts
"""
import os
import shutil
import sys

def _dedup_hosts_file(file:str) -> dict[str, tuple[str, str]]:
    with open(file) as fd:
        lines = fd.readlines()
    pubkeys:dict[str, tuple[str, str]] = {}
    for line in lines:
        host, algo, pubkey = line.split()
        if pubkey in pubkeys.keys():
            print(f"{pubkey=} exists. Remove the old host {pubkeys[pubkey][0]}.\n")
        pubkeys[pubkey] = (host, algo)
    return pubkeys

def _write_hosts(host_entry:dict[str, tuple[str, str]], file:str):
    with open(file, "w") as host:
        for pubkey, (hs, algo) in host_entry.items():
            host.write(f"{hs} {algo} {pubkey}\n")

def dedup_hosts_by_fingerprint(
        known_hosts:str=os.path.expanduser("~/.ssh/known_hosts")
    ):
    hosts_old = known_hosts+".old"
    shutil.copy(known_hosts, hosts_old)
    print(f"copy {known_hosts} to {hosts_old}")

    pubkeys = _dedup_hosts_file(known_hosts)
    _write_hosts(pubkeys, known_hosts)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("too much arguments!")
    elif len(sys.argv) == 2:
        dedup_hosts_by_fingerprint(sys.argv[1])
    else:
        dedup_hosts_by_fingerprint()
