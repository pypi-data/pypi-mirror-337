from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="jupyterhub-enverge-gpu-check",
    version="0.0.1",
    description="JupyterHub GPU Resource Usage Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enverge-Labs/gpu_check",
    author="Tudor M",
    author_email="tudor@enverge.ai",
    license="3 Clause BSD",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "jupyterhub>=4.1.6",
        "tornado>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
    include_package_data=True,
) 