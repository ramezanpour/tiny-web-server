from datetime import datetime
from config import Config

import os
import mimetypes


class Response:
    def __init__(self, root_path, request):
        self._root = root_path
        self._request = request
        self.http_version = self._request.http_version
        self._set_status(200)
        self.encoding = 'utf-8'
        self._set_payload('Success')
        self._response = []

    @property
    def status_codes(self):
        return {
            200: '200 OK',
            201: '201 Created',
            204: '204 No Content',

            301: '301 Moved Permanently',

            400: '400 Bad Request',
            401: '401 Unauthorized',
            403: '403 Forbidden',
            409: '409 Conflict',
            404: '404 Not Found',
            500: '500 Internal Server Error',
        }

    def _set_status(self, code):
        self.status = self.status_codes[code]
        self.status_code = code

    def _set_payload(self, payload, content_type='text/plain'):
        self.payload = payload
        self.content_type = content_type

    def _set_not_found(self):
        self.payload = b'<h1>Resource cannot be found :(</h1>'
        self.content_type = 'text/html'
        self._set_status(404)

    def _is_requested_file_binary(self, mime) -> bool:
        mime = mime.lower()
        # TODO: Need more accurate binary detection
        if mime.startswith('text') or mime == 'application/json':
            return False
        return True

    def _prepare_requested_file(self):
        full_path = f'{self._root}{self._request.url}'
        if not os.path.exists(full_path):
            self._set_not_found()
        else:
            if os.path.isdir(full_path):
                has_default_document = False
                files_in_directory = os.listdir(full_path)
                for f in files_in_directory:
                    if f in Config['defaultDocuments']:
                        full_path = os.path.join(full_path, f)
                        has_default_document = True
                if not has_default_document:
                    self._set_not_found()
                    return

            mime = mimetypes.guess_type(full_path)[0]
            is_binary = self._is_requested_file_binary(mime)

            with open(full_path, 'rb' if is_binary else 'r') as file:
                self._set_payload(file.read(), mime)

    def _add_headers_to_response(self):
        self._response.append(f'{self.http_version} {self.status}')
        self._response.append(f'Date: {datetime.now().ctime()}')
        self._response.append(f'Server: {Config["name"]}/{Config["version"]}')
        self._response.append(f'Last-Modified: {datetime.now().ctime()}')
        self._response.append(
            f'Content-Type: {self.content_type}; charset={self.encoding}')
        self._response.append(f'Content-Length: {len(self.payload)}')
        self._response.append('\r\n')

    def get_response(self) -> bytes:
        self._prepare_requested_file()
        self._add_headers_to_response()

        result = '\r\n'.join(self._response)
        if not isinstance(self.payload, bytes):
            self.payload = self.payload.encode('utf-8')
        result = result.encode('utf-8') + self.payload
        return result
