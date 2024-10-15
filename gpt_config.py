import os

gen_query_model = "gemma-2-2b-jpn-q8:latest"
html_parse_model = "gemma-2-2b-jpn-q8:latest"
abstract_parse_model = "gemma-2-2b-jpn-q8:latest"
pdf_extraction_model = "gemma-2-2b-jpn-q8:latest"


def get_driver_path():
    if os.name == "nt":
        return "driver/chromedriver.exe"
    else:
        return "driver/chromedriver"
