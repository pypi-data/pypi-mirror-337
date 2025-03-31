from setuptools import setup, find_packages

setup(
    name="date_day_estimator",
    version="0.0.3",
    description="To estimate the day of the week from date/month/year info",
    author="Mayur Waghchoure",
    packages= find_packages(),
    install_requires = [
        'numpy',
    ],
    url='https://github.com/Mayakshanesht/date_day_estimator_pypi_package',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],

)