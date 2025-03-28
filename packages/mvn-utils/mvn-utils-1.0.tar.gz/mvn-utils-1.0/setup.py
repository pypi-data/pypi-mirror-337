from setuptools import setup, find_packages

setup(
    name="mvn-utils",
    version="1.0",
    keywords=("mvn utils", "java dependencies"),
    description="code sdk",
    long_description="tools for re",
    license="MIT Licence",

    url="https://xxx.com",
    author="xuwuqiang",
    author_email="xwqiang2008@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["setuptools==65.6.3"],

    scripts=[],
    # 如果出现 ModuleNotFoundError: No module named,用 py_modules
    py_modules=[],
    entry_points={
        'console_scripts': [
            'dependency = main:mvn_graph_command'
        ]
    }
)
