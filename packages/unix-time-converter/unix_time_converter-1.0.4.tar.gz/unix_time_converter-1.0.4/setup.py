from setuptools import setup


setup(
    name='unix-time-converter',
    version='1.0.4',
    author='Franz Wiesinger',
    author_email='py@roadrunnerserver.com',
    description='application for converting local time or UTC into Unixtime \
        and viceversa',
    url='https://docs.roadrunnerserver.com/unixtime/html/index.html',
    # license_files=('LICENSE.md'),
    packages=[
        'res',
        'tests'
    ],
    install_requires=[
        'datetime', 'pytz', 'tkhtmlview'
    ],
    python_requires='>= 3.9',
    entry_points={
        'gui_scripts': [
            'unixtime = unixtime.__main__:unixtime'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords=[
        'unixtime', 'utc', 'local time', 'the epoch', 'converter', 'tkinter',
        'GUI', 'timezone', 'datetime'
    ]
)
