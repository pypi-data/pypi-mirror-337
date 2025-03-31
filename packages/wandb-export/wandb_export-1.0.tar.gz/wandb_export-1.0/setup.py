from setuptools import setup, find_namespace_packages

setup(
    name="wandb-export",
    url="https://github.com/tboulet/Wandb-Export",
    author="Timothé Boulet",
    author_email="timothe.boulet0@gmail.com",
    packages=find_namespace_packages(),
    version="1.0",
    license="MIT",
    description="A package to export runs from a WandB project to a local folder.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "wandb-export             = wandb_export.export:main",
            "wandb-export-init-config = wandb_export.init_config:main",
        ],
    },
)
