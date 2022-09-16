import setuptools

setuptools.setup(
    name='novel_swarms',
    version='0.0.1',
    author='Connor Mattson',
    author_email='c.mattson@utah.edu',
    description='Simulation and Evolution on Computation Free Swarms',
    long_description='Simulation and Evolution on Computation Free Swarms',
    url='https://github.com/Connor-Mattson/NovelSwarmBehavior',
    project_urls={
        "Bug Tracker": "https://github.com/Connor-Mattson/NovelSwarmBehavior/issues"
    },
    license='MIT',
    packages=[
        "cycler==0.11.0",
        "fonttools==4.35.0",
        "joblib==1.1.0",
        "kiwisolver==1.4.4",
        "matplotlib==3.5.3",
        "numpy==1.23.1",
        "packaging==21.3",
        "Pillow==9.2.0",
        "pygame==2.1.2",
        "pyparsing==3.0.9",
        "python-dateutil==2.8.2",
        "scikit-learn==1.1.2",
        "scikit-learn-extra==0.2.0",
        "scipy==1.9.0",
        "six==1.16.0",
        "threadpoolctl==3.1.0",
    ],
    install_requires=["pygame==2.1.2"],
)
