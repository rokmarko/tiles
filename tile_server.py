#!/usr/bin/env python3
"""
tile_server.py — minimal static file server for MapLibre tile serving.

Serves style.json, fonts, sprites, and .pbf tiles from a directory tree,
setting Content-Encoding: gzip on .pbf files since browsers/MapLibre won't
decompress them otherwise if they were pre-gzipped by Planetiler/Tippecanoe.

Usage:
    ./tile_server.py [directory] [port]
    ./tile_server.py ./tileserver 8080
"""

import sys
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class TileHandler(SimpleHTTPRequestHandler):
    # Extend the extension->mimetype map so .pbf isn't served as
    # application/octet-stream (still fine for MapLibre, but explicit is better).
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".pbf": "application/x-protobuf",
        ".json": "application/json",
    }

    def end_headers(self):
        # CORS — needed since MapLibre in a browser/artifact context will be
        # a different origin than this file server.
        self.send_header("Access-Control-Allow-Origin", "*")

        # Declare gzip encoding ONLY for .pbf files, and only if they are
        # actually gzip-compressed on disk (check magic bytes rather than
        # assuming, since Tippecanoe folder output is uncompressed by default
        # while Planetiler/mb-util output usually is gzipped).
        if self.path.endswith(".pbf"):
            filepath = self.translate_path(self.path)
            if os.path.isfile(filepath) and self._is_gzip(filepath):
                self.send_header("Content-Encoding", "gzip")

        super().end_headers()

    @staticmethod
    def _is_gzip(filepath):
        try:
            with open(filepath, "rb") as f:
                return f.read(2) == b"\x1f\x8b"
        except OSError:
            return False

    def log_message(self, format, *args):
        # Quieter default logging; comment out to get full request logs.
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

    os.chdir(directory)
    handler = TileHandler
    server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    print(f"Serving {os.getcwd()} on http://localhost:{port} (Content-Encoding: gzip on .pbf detected as gzip)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()

