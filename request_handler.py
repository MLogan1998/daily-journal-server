from http.server import BaseHTTPRequestHandler, HTTPServer

from entries import get_all_entries, get_single_entry, delete_entry
from moods import get_all_moods, get_single_mood


# Here's a class. It inherits from another class.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
      # Just like splitting a string in JavaScript. If the
      # path is "/animals/1", the resulting list will
      # have "" at index 0, "animals" at index 1, and "1"
      # at index 2.
      path_params = path.split("/")
      resource = path_params[1]
      id = None

      # Try to get the item at index 2
      try:
          id = int(path_params[2])
      except IndexError:
          pass  # No route parameter exists: /animals
      except ValueError:
          pass  # Request had trailing slash: /animals/

      return (resource, id) 

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            if id is not None:
                response = f"{get_single_entry(id)}"

            else:
                response = f"{get_all_entries()}"
        
        elif resource == "moods":
            if id is not None:
                response = f"{get_single_mood(id)}"
            
            else:
                response = f"{get_all_moods()}"

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        response = f"received post request:<br>{post_body}"
        self.wfile.write(response.encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        self.do_POST()
    

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
