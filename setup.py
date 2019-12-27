from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("hlsubleq/version.py", "r") as f:
    exec(f.read(), globals())

setup(
    name = "hl-subleq-tools",
    description = "'high-level' subleq assembler and simulator",
    version = __version__,
    author = "Ferdinand Bachmann",
    author_email = "theferdi265@gmail.com",
    packages = ["hlsubleq", "hlsubleq.cli"],
    entry_points = {
        "console_scripts": [
            "subleq-asm=hlsubleq.cli.asm:main",
            "subleq-hlasm=hlsubleq.cli.hlasm:main",
            "subleq-sim=hlsubleq.cli.sim:main",
            "subleq-hlsim=hlsubleq.cli.hlsim:main",
        ]
    },
    python_requires = ">=3.5",
    install_requires = requirements
)
