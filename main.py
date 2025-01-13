from website import create_app

app = create_app()

# The code within this statement is only run if 'main.py' itself is run
# ie: the code within will not run if this file is imported elsewhere
if __name__ == '__main__':
    # 'debug=True' - The virtual server updates every time the source code is modified
    app.run(debug=True)
