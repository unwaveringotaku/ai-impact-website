import os
from urllib.parse import quote
from html.parser import HTMLParser


class ImgSrcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            for attr, value in attrs:
                if attr.lower() == "src":
                    self.srcs.append(value)


def get_img_sources(html_path):
    parser = ImgSrcParser()
    with open(html_path, "r", encoding="utf-8") as f:
        parser.feed(f.read())
    return parser.srcs


def test_all_image_files_exist():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_file = os.path.join(project_root, "index.html")
    srcs = get_img_sources(html_file)

    missing = []
    for src in srcs:
        # remove leading slashes and known prefix
        if src.startswith("/mnt/data/"):
            src = src[len("/mnt/data/") :]
        src = src.lstrip("/")
        encoded_src = quote(src, safe="")
        file_path = os.path.join(project_root, encoded_src)
        if not os.path.exists(file_path):
            missing.append(src)

    assert not missing, f"Missing files: {missing}"
