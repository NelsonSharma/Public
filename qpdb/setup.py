from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name =          'qpdb',
    version =       '0.0.1',  # 0.0.x is for unstable versions
    url =           "https://github.com/Nelson-iitp/qpdb",
    author =        "Nelson.S",
    author_email =  "mail.nelsonsharma@gmail.com",
    description =   'qpdb',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #py_modules =    [""],
    packages =      ['qpdb'],
    license =       'Apache2.0',
    package_dir =   { '' : 'src'},
    install_requires = [],
    include_package_data=True
)

# cd ..../src
# python38 -m build
# python38 -m twine upload dist/*
# NelsonSharma