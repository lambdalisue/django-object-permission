# vim: set fileencoding=utf8:
from setuptools import setup, find_packages

version = '0.5.2'

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="django-object-permission",
    version=version,
    description = "Add object specific permission for particualr User/Group, All authenticated user or Anonymous user",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django permission object",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-object-permission",
    download_url = r"https://github.com/lambdalisue/django-object-permission/tarball/master",
    license = 'MIT',
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'distribute',
        'setuptools-git',
        'django>=1.3',
        'django-observer>=0.3rc3',
    ],
    test_suite='runtests.runtests',
    tests_require=[
        'PyYAML',
    ],
)
