from setuptools import setup, find_namespace_packages


setup(
    name="kognic-studio-proto",
    packages=find_namespace_packages(include=["kognic.*"], where="src/main/python"),
    package_dir={"": "src/main/python"},
    version="v0.0.21",
    author="Kognic",
    author_email="team-annotate@kognic.com",
    install_requires=["protobuf"],
    python_requires="~=3.10",
    scripts=[],
    package_data={"": ["*.pyi"]}
)
