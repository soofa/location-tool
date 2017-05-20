from setuptools import setup

setup(
    name='location_tool',
    packages=['location_tool'],
    include_package_data=True,
    install_requires=[
        'flask',
        'numpy',
        'yelp',
        'googlemaps',
        'python-dotenv',
    ],
)
