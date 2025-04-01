from setuptools import setup, find_packages

version = {}
with open("pdf_reports/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="pdf_reports",
    version=version["__version__"],
    author="Zulko",
    url="https://github.com/Edinburgh-Genome-Foundry/pdf_reports",
    description="Create nice-looking PDF reports from HTML content.",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    keywords="PDF report web jinja weasyprint",
    packages=find_packages(exclude="docs"),
    include_package_data=True,
    install_requires=[
        "pypugjs",
        "jinja2",
        "weasyprint",
        "beautifulsoup4",
        "pandas",
        "Markdown",
        "backports.functools-lru-cache",
    ],
)
