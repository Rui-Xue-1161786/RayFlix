from __init__ import create_app


def main():
    app = create_app()
    app.run(host='localhost', port=8000, threaded=False,debug=True)


if __name__ == "__main__":
    main()