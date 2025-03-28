from setuptools import setup, find_packages

setup(
    name="mvn-utils",
    version="1.0.6",
    keywords=("mvn utils", "java dependencies"),
    description="code sdk",
    long_description="""
    command line tool for maven dependencies
    
    usage:
    dependency -d 'your mvn project path' 
    
    use mmdc to generate graph, you need to install mermaid-cli first, use command:
    
    npm install -g @mermaid-js/mermaid-cli
    
    """,
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
            'dependency = mvn.main:mvn_graph_command'
        ]
    }
)
