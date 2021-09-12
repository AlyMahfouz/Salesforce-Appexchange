from setuptools import setup

# pip install pip-tools
# pip-compile
# pip install -r requirements.txt

setup(
    name='SFScrape',
    version='0.1',
    license='GPL3',
    author='Aly Mahfouz',
    author_email='aly.mahfouz14@gmail.com',
    description='SF Scraping Tool',
    install_requires=[
 
        # Scraping Tools
        
        'beautifulsoup4',
        'selenium',
        'requests',
        'numpy',
        'pandas'

    ]
)
