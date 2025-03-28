from setuptools import setup, find_packages

with open("pyicon/version.py", 'r') as f:
    version = f.read() 
    version = version.split('=')[1].replace(' ', '').replace('"', '').replace('\n', '')

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

with open("requirements_documentation.txt") as f:
    documentation_requires = f.read().strip().split("\n")

with open("requirements_development.txt") as f:
    development_requires = f.read().strip().split("\n")

setup(
    name='pyicon-diagnostics',
    version=version,
    description='Diagnostic python software package for ICON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.dkrz.de/m300602/pyicon',
    author='The pyicon development team',
    author_email='nils.brueggemann@mpimet.mpg.de',
    install_requires=install_requires,
    extras_require={
        "dev": development_requires,
        "doc": documentation_requires,
        "full": development_requires+documentation_requires,
    },
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyic_intake = scripts.pyic_intake:main',
            'pyic_fig = scripts.pyic_fig:main',
            'pyic_sec = scripts.pyic_sec:main',
            'pyic_anim = scripts.pyic_anim:main',
            'pyic_view = scripts.pyic_view:main',
       ],
    },
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
    ],
    setup_requires=['setuptools'],
)
