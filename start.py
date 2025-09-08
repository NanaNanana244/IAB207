from templates import app

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8023,
        host='0.0.0.0'
    )