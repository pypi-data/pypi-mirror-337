from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terminal-snake-game",
    version="1.0.0",
    author="Sweta Tanwar",
    author_email="shweta_tanwar@ymail.com",
    description="A colorful terminal-based Snake game with score tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwetaTanwar/snake-game",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "snake-game=snake_game:main",
        ],
    },
    py_modules=["snake_game"],
) 