#!/usr/bin/env python3
# server.py
# 🌐 BEAUTIFUL VANILLA JS INTERFACE SERVER 🌐

import http.server
import socketserver
import webbrowser
import threading
import time
import os
from pathlib import Path

class GraphyBOOKServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        
    def start_server(self):
        """Start the beautiful web interface server"""
        
        # Change to web_studio directory
        web_dir = Path(__file__).parent
        os.chdir(web_dir)
        
        print("🌐 Starting GraphyBOOK Beautiful Web Interface...")
        print("=" * 60)
        print(f"🚀 Server starting on port {self.port}")
        print(f"📁 Serving from: {web_dir}")
        print("🌌 Landing page with galaxy animation ready!")
        print("=" * 60)
        
        # Create custom handler to serve templates.html as default
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.path = '/templates.html'
                return super().do_GET()
        
        handler = CustomHandler
        
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                self.server = httpd
                
                print(f"✅ Server running at: http://localhost:{self.port}")
                print("🎨 Beautiful black theme with gradient title")
                print("📱 Perfect split-screen layout")
                print("🚀 Ready for physics animations!")
                print("=" * 60)
                print("💡 Press Ctrl+C to stop the server")
                print("=" * 60)
                
                # Open browser after a short delay
                threading.Thread(target=self.open_browser_delayed, daemon=True).start()
                
                # Start serving
                httpd.serve_forever()
                
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def open_browser_delayed(self):
        """Open browser after server starts"""
        time.sleep(2)
        print("🌐 Opening browser...")
        try:
            webbrowser.open(f'http://localhost:{self.port}')
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")
            print(f"📱 Manually open: http://localhost:{self.port}")

def main():
    """Main function to start the beautiful interface"""
    
    print("""
🖤 GRAPHYBOOK BEAUTIFUL WEB INTERFACE 🖤

Features:
✨ Stunning black theme with blue-purple gradient
🎯 Perfect 50/50 split screen layout  
🧠 AI Prompt mode for physics concepts
💻 Manual Code mode for direct input
🎬 Beautiful video display area
📱 Fully responsive design
⚡ Vanilla JS - No frameworks needed!

Starting server...
""")
    
    # Check if port is provided as argument
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    
    server = GraphyBOOKServer(port=port)
    server.start_server()

if __name__ == "__main__":
    main()