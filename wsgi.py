from app import app

# Vercel sẽ tự động detect wsgi.py và sử dụng app object
application = app

if __name__ == "__main__":
    app.run()
