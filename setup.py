from setuptools import setup

setup(
    name='location_tool',
    packages=['location_tool'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'psycopg2',
        'numpy',
        'yelp',
        'googlemaps',
        'python-dotenv',
        'celery',
    ],
)
