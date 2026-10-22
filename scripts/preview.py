#!/usr/bin/env python3
"""Serve built pages locally, including GitHub Pages extensionless HTML routes."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'_site'
class Preview(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def translate_path(self,path):
        resolved=super().translate_path(path)
        html=Path(resolved+'.html')
        if not Path(resolved).exists() and html.is_file(): return str(html)
        return resolved
if __name__=='__main__':
    print('Preview: http://127.0.0.1:4173',flush=True)
    ThreadingHTTPServer(('127.0.0.1',4173),Preview).serve_forever()
