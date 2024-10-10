import http.server
import socketserver
import os
import argparse

def run_server(port, path):
    # Check if the path is a file or directory
    if os.path.isfile(path):
        directory, filename = os.path.split(path)
        os.chdir(directory)
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.path = '/' + filename
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
        handler = CustomHandler
    else:
        os.chdir(path)
        handler = http.server.SimpleHTTPRequestHandler

    # Create the server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        if os.path.isfile(path):
            print(f"Serving file: {filename}")
        print(f"Press CTRL+C to stop the server")
        
        # Serve until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--dir", type=str, default=".", help="Directory or file to serve (default: current directory)")
    
    # Parse the arguments
    args = parser.parse_args()

    # Run the server
    run_server(args.port, args.dir)
