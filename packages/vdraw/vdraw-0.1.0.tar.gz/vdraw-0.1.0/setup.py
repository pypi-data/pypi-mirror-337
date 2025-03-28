from setuptools import setup, find_packages

setup(
    name="vdraw",
    version="0.1.0",
    description="A library for working with segmentation masks",
    author="Arturs Vitins",
    author_email="workerlv@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
