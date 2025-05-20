Interactive script to use a given wav file, split it based on detected silence of given length and db, and export as many files as there are detected segments. Length and step size are in ms, not in seconds. 1000ms = 1s

Run using something like: python -m main

Requires pydub, install via: pip install pydub.

If you want to keep your system python unmodified, create venv before using pip and activate. The following commands do this:

python -m venv venv

source venv/Scripts/activate (if Windows) source venv/bin/activate (unix OS)

which pip (To ensure we use venv pip)

pip install pydub
