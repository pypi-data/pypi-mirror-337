import logging
import geopandas as gpd
from pathlib import Path
from django.utils.deprecation import MiddlewareMixin
from django.core.files.uploadedfile import SimpleUploadedFile

logger = logging.getLogger(__name__)


class GeoExplodeMiddleware(MiddlewareMixin):
    """
    Transform a geojson file received via geopandas
    Explodes MultiType geometries to singe Types
    """

    def process_request(self, request):
        if request.method=="POST" and 'multipart/form-data' in request.content_type:
            for key, content in request.FILES.items():
                if Path(content.name).suffix.lower() == ".geojson":
                    try:
                        gdf = gpd.read_file(content.file)
                        exploded_gdf = gdf.explode(ignore_index=True)
                        new_content = exploded_gdf.to_json(to_wgs84=True).encode()
                        new_file = SimpleUploadedFile(
                            name=content.name,
                            content=new_content,
                            content_type=content.content_type
                        )
                        request.FILES[key] = new_file

                    except Exception as e:
                        logger.info(f"Something went wrong {e}")
                        pass

        return self.get_response(request)
