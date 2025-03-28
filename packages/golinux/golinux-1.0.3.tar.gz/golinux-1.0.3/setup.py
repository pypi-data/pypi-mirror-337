from setuptools import setup, find_packages

setup(
    name="golinux",
    version="1.0.3",
    author="Unionium NCO",
    author_email="golinux@unionium.org",
    description="#GoLinux",
    long_description="# #Go Linux!\n A library that shows Linux propaganda when imported on Windows",
    long_description_content_type="text/markdown",
    url="https://github.com/unionium/#golinux",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama; platform_system=='Windows'",
    ],
    keywords="linux windows propaganda",
    project_urls={
        "Bug Reports": "https://github.com/unionium/#golinux/issues",
        "Source": "https://github.com/unionium/#golinux",
    },
)