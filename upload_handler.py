#!/usr/bin/env python3
import os
import sys
import json
import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import BytesIO

DOWNLOAD_DIR = 'downloads'
CSV_FILE = 'data/resources.csv'

class UploadHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/software/list':
            self.send_software_list()
        else:
            self.serve_static_file()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/software/upload':
            self.handle_upload()
        elif path == '/api/software/delete':
            self.handle_delete()
        else:
            self.send_error(404, 'Not Found')

    def send_software_list(self):
        software_list = []
        
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    download_url = row.get('下载链接', row.get('download_url', ''))
                    if download_url and 'downloads/' in download_url:
                        software_list.append({
                            'id': row.get('资源ID', row.get('id', '')),
                            'title': row.get('标题', row.get('title', '')),
                            'version': row.get('版本', row.get('version', '')),
                            'fileSize': row.get('文件大小', row.get('file_size', '')),
                            'downloadUrl': download_url,
                            'description': row.get('一句话简介', row.get('description', '')),
                            'icon': row.get('图标', row.get('icon', '⚙️')),
                            'badge': row.get('角标', row.get('badge', ''))
                        })
        
        self.send_json(200, {'success': True, 'data': software_list})

    def handle_upload(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json(400, {'success': False, 'message': 'No content'})
            return

        content_type = self.headers.get('Content-Type', '')
        
        if 'multipart/form-data' in content_type:
            self.handle_multipart_upload(content_length)
        else:
            self.send_json(400, {'success': False, 'message': 'Unsupported content type'})

    def handle_multipart_upload(self, content_length):
        boundary = self.headers.get('Content-Type').split('boundary=')[1]
        data = self.rfile.read(content_length)
        
        parts = data.split(b'--' + boundary.encode())
        file_data = None
        file_name = ''
        fields = {}
        
        for part in parts:
            if b'Content-Disposition' in part:
                lines = part.split(b'\r\n')
                disp_line = [l for l in lines if b'Content-Disposition' in l][0]
                
                if b'filename=' in disp_line:
                    file_name = disp_line.decode().split('filename=')[1].strip('"')
                    content_start = part.find(b'\r\n\r\n') + 4
                    content_end = part.rfind(b'\r\n--')
                    file_data = part[content_start:content_end]
                else:
                    name_match = disp_line.decode().split('name=')[1].strip('"')
                    content_start = part.find(b'\r\n\r\n') + 4
                    content_end = part.rfind(b'\r\n--')
                    fields[name_match] = part[content_start:content_end].decode('utf-8')
        
        if not file_data or not file_name:
            self.send_json(400, {'success': False, 'message': 'No file uploaded'})
            return

        name = fields.get('name', '')
        version = fields.get('version', '')
        desc = fields.get('description', '')
        icon = fields.get('icon', '⚙️')
        
        if not name or not version or not desc:
            self.send_json(400, {'success': False, 'message': 'Missing required fields'})
            return

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        file_ext = file_name.split('.')[-1]
        save_name = f"{name.replace(' ', '-')}-{version}.{file_ext}"
        save_path = os.path.join(DOWNLOAD_DIR, save_name)
        
        with open(save_path, 'wb') as f:
            f.write(file_data)

        download_url = f'downloads/{save_name}'
        file_size = self.format_size(len(file_data))
        
        self.update_csv(name, version, desc, icon, file_size, download_url)
        
        self.send_json(200, {
            'success': True,
            'message': 'Upload successful',
            'data': {
                'name': name,
                'version': version,
                'fileSize': file_size,
                'downloadUrl': download_url
            }
        })

    def handle_delete(self):
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            params = json.loads(data)
            url = params.get('url', '')
            
            if not url:
                self.send_json(400, {'success': False, 'message': 'No URL provided'})
                return
            
            file_path = url.replace('/', os.sep)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            self.send_json(200, {'success': True, 'message': 'Deleted'})
        
        except json.JSONDecodeError:
            self.send_json(400, {'success': False, 'message': 'Invalid JSON'})

    def update_csv(self, name, version, desc, icon, file_size, download_url):
        rows = []
        headers = ['资源ID', '分类ID', '标题', '网址', '一句话简介', '图标', '角标', '启用', '排序', '版本', '文件大小', '下载链接']
        
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                existing_headers = next(reader)
                if len(existing_headers) > 0:
                    headers = existing_headers
                rows.extend(list(reader))
        
        new_id = name.lower().replace(' ', '-').replace('[^a-z0-9-]', '')
        new_row = [
            new_id,
            'tools',
            name,
            version,
            desc,
            icon,
            '推荐',
            '1',
            str(len(rows) + 1),
            version,
            file_size,
            download_url
        ]
        
        rows.append(new_row)
        
        with open(CSV_FILE, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def format_size(self, bytes):
        if bytes == 0:
            return '0 Bytes'
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB']
        i = 0
        while bytes >= k and i < len(sizes) - 1:
            bytes /= k
            i += 1
        return f'{bytes:.2f} {sizes[i]}'

    def serve_static_file(self):
        path = self.path
        if path == '/':
            path = '/index.html'
        
        file_path = os.path.join(os.getcwd(), path.lstrip('/'))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'text/javascript',
                '.json': 'application/json',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon',
                '.csv': 'text/csv',
                '.txt': 'text/plain',
                '.exe': 'application/octet-stream',
                '.zip': 'application/zip',
                '.rar': 'application/x-rar-compressed',
                '.dmg': 'application/x-apple-diskimage',
                '.pkg': 'application/x-newton-compatible-pkg'
            }
            
            content_type = content_types.get(ext, 'application/octet-stream')
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            if ext in ['.exe', '.zip', '.rar', '.dmg', '.pkg']:
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, 'File not found')

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    port = 8000
    server = HTTPServer(('0.0.0.0', port), UploadHandler)
    print(f'Starting server on port {port}...')
    print(f'Open http://localhost:{port} in your browser')
    print(f'Admin page: http://localhost:{port}/admin-upload.html')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped')
        server.server_close()

if __name__ == '__main__':
    main()