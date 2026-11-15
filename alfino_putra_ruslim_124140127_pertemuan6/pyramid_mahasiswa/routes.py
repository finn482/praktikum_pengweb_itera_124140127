"""URL Dispatch untuk seluruh endpoint aplikasi."""


def includeme(config):
    """Mendaftarkan route home dan REST API Mahasiswa."""
    config.add_route("home", "/", request_method="GET")

    config.add_route(
        "mahasiswa_list", "/api/mahasiswa", request_method="GET"
    )
    config.add_route(
        "mahasiswa_detail", "/api/mahasiswa/{id}", request_method="GET"
    )
    config.add_route(
        "mahasiswa_add", "/api/mahasiswa", request_method="POST"
    )
    config.add_route(
        "mahasiswa_update", "/api/mahasiswa/{id}", request_method="PUT"
    )
    config.add_route(
        "mahasiswa_delete", "/api/mahasiswa/{id}", request_method="DELETE"
    )
