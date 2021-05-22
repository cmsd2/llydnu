#!/usr/bin/env python3

from collections import namedtuple
from urllib import request
import os
import subprocess
import sys

rust_version = "1.52.1"
rustup_version = "1.24.1"

LambdaArch = namedtuple("LambdaArch", ["bashbrew", "yum", "rust"])

lambda_arches = [
    LambdaArch("amd64", "x86_64", "x86_64-unknown-linux-gnu"),
]

lambda_variants = [
    "al2"
]

default_lambda_variant = "al2"

def rustup_hash(arch):
    url = f"https://static.rust-lang.org/rustup/archive/{rustup_version}/{arch}/rustup-init.sha256"
    with request.urlopen(url) as f:
        return f.read().decode('utf-8').split()[0]

def read_file(file):
    with open(file, "r") as f:
        return f.read()

def write_file(file, contents):
    dir = os.path.dirname(file)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    with open(file, "w") as f:
        f.write(contents)


def update_lambda():
    arch_case = 'yumArch="$(arch)"; \\\n'
    arch_case += '    case "${yumArch##*-}" in \\\n'
    for arch in lambda_arches:
        hash = rustup_hash(arch.rust)
        arch_case += f"        {arch.yum}) rustArch='{arch.rust}'; rustupSha256='{hash}' ;; \\\n"
    arch_case += '        *) echo >&2 "unsupported architecture: ${yumArch}"; exit 1 ;; \\\n'
    arch_case += '    esac'

    template = read_file("Dockerfile-lambda.template")

    for variant in lambda_variants:
        rendered = template \
            .replace("%%RUST-VERSION%%", rust_version) \
            .replace("%%RUSTUP-VERSION%%", rustup_version) \
            .replace("%%AMAZON-LINUX%%", variant) \
            .replace("%%ARCH-CASE%%", arch_case)
        write_file(f"{rust_version}/lambda/{variant}/Dockerfile", rendered)


def update_travis():
    file = ".travis.yml"
    config = read_file(file)

    versions = ""
    for variant in debian_variants:
        versions += f"  - VERSION={rust_version} VARIANT={variant}\n"
        versions += f"  - VERSION={rust_version} VARIANT={variant}/slim\n"

    for version in alpine_versions:
        versions += f"  - VERSION={rust_version} VARIANT=alpine{version}\n"

    marker = "#VERSIONS\n"
    split = config.split(marker)
    rendered = split[0] + marker + versions + marker + split[2]
    write_file(file, rendered)


def file_commit(file):
    return subprocess.run(
            ["git", "log", "-1", "--format=%H", "HEAD", "--", file],
            capture_output = True) \
        .stdout \
        .decode('utf-8') \
        .strip()


def version_tags():
    parts = rust_version.split(".")
    tags = []
    for i in range(len(parts)):
        tags.append(".".join(parts[:i + 1]))
    return tags


def single_library(tags, architectures, dir):
    return f"""
Tags: {", ".join(tags)}
Architectures: {", ".join(architectures)}
GitCommit: {file_commit(os.path.join(dir, "Dockerfile"))}
Directory: {dir}
"""


def usage():
    print(f"Usage: {sys.argv[0]} update")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    task = sys.argv[1]
    if task == "update":
        update_lambda()
    else:
        usage()
