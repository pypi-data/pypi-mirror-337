import setuptools
import glob
from setuptools import setup, find_packages

packages = find_packages(
    exclude=["benchmarks", "clibs", "data", "demo", "dist", "doc", "docs", "logs", "models", "test", "figures"]
)
print("packages:", packages)

# Find all matching files
# This returns a list of file paths like "rgl/graph_retrieval/libretrieval.cpython-310-x86_64-linux-gnu.so"
package_files = glob.glob("rgl/graph_retrieval/libretrieval.cpython-3*-x86_64-linux-gnu.so")

description = "RGL - RAG-on-Graphs Library"
try:
    long_description = open("README.md", "r", encoding="utf-8").read()
except Exception:
    long_description = description

# Adjust paths to be relative to the package directory ("rgl").
# That is, remove the leading "rgl/" portion.
relative_files = [f[len("rgl/") :] for f in package_files]

setup(
    name="rgl",
    python_requires=">3.7.0",
    version="0.0.4",
    author="anthonynus",
    author_email="e0403849@u.nus.edu",
    packages=packages,
    install_requires=["ogb", "patool", "faiss-cpu", "rouge-score", "gradio"],
    # extras_require={"torch-2.4": ["dgl @ https://data.dgl.ai/wheels/torch-2.4/dgl-0.9.0-cp38-cp38-linux_x86_64.whl"]},
    package_data={"rgl": relative_files},
    description=description,
    license="GNU General Public License v3.0 (See LICENSE)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyRGL/rgl",
)
