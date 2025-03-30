from setuptools import setup, find_packages

with open("src/docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terminal_snake_game",
    version="1.0.4",
    author="Sweta Tanwar",
    author_email="shweta_tanwar@ymail.com",
    description="A classic Snake game implementation in Python using curses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwetaTanwar/snake-game",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'snake-game=terminal_snake_game:main',
        ],
    },
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
) 