"""View sederhana untuk endpoint root."""

from pyramid.view import view_config


@view_config(route_name="home", renderer="json")
def home_view(request):
    """Mengembalikan informasi singkat API."""
    return {
        "name": "Pyramid REST API Mahasiswa dan Matakuliah",
        "status": "running",
    }
