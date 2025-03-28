from setuptools import find_packages, setup

setup(
    name="b15py",
    packages=find_packages(include=["b15py"]),
    version="1.0.3",
    description="Ein Module um das B15F-Board mit Python zu programmieren.",
    author="mmeiler-dev",
    install_requires=[
        "pyserial>=3.5",
        "typeguard>=4.4.1"
    ]
)
