from setuptools import find_packages, setup

requires = [
    "alembic",
    "psycopg2-binary",
    "pyramid",
    "pyramid_tm",
    "SQLAlchemy",
    "transaction",
    "waitress",
    "zope.sqlalchemy",
]

tests_require = ["pytest", "WebTest"]

setup(
    name="pyramid_mahasiswa",
    version="1.0.0",
    description="RESTful API Mahasiswa dan Matakuliah dengan Pyramid",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={"testing": tests_require},
    entry_points={
        "paste.app_factory": ["main = pyramid_mahasiswa:main"],
        "console_scripts": [
            "initialize_pyramid_mahasiswa_db = "
            "pyramid_mahasiswa.scripts.initialize_db:main",
        ],
    },
)
