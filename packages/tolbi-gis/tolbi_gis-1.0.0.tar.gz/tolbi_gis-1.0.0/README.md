# Django GeoJSON Explode Middleware

A Django middleware that automatically explodes GeoJSON geometries in POST requests.

## Installation

```bash
pip install tolbi-gis
```

## Usage

1. **Add the middleware to your `settings.py`:**

    ```python
    MIDDLEWARE = [
        # ... other middleware ...
        'tolbi.middleware.GeoExplodeMiddleware',
        # ... other middleware ...
    ]
    ```

2. **Send GeoJSON data in your POST requests:**

    The middleware will process POST requests `content-type: multipart/form-data`.

## What it does

This middleware intercepts incoming POST requests and checks for GeoJSON file (.geojson). If found, it uses GeoPandas to "explode" multi-part geometries (e.g., MultiPolygon, MultiLineString) into individual geometries. The exploded GeoJSON is then made available in the request data, simplifying the processing of complex geospatial data in your Django views.

## Dependencies

- Django (>= 3.2)
- geopandas

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[MIT License](LICENSE)
