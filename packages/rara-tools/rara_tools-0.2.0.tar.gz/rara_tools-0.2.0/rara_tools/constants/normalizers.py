from pymarc import Indicators
import os

EMPTY_INDICATORS = Indicators(" ", " ")
VIAF_ALLOWED_SOURCES = ["LC", "DNB", "LNB", "NLL",
                        "ERRR", "J9U"]

ES_HOST = os.getenv("ELASTIC_TEST_URL", "http://localhost:9200")

LINKER_CONFIG = {
    "add_viaf_info": True,
    "vectorizer_data_path": "./vectorizer_data",
    "per_config": {"es_host": ES_HOST},
    "org_config": {"es_host": ES_HOST},
    "loc_config": {"es_host": ES_HOST},
    "ems_config": {"es_host": ES_HOST},
}
