from setuptools import setup, find_packages

setup(
    name="django-invoice-library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2"
    ],
    include_package_data=True,
    license="MIT",
    description="A Django-based invoice generation library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/django-invoice-library",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
)
