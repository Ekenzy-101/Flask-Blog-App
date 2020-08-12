from flaskblog import create_app
from flaskblog.commands import create_tables

app = create_app()
app.cli.add_command(create_tables)

if __name__ == "__main__":
    app.run(debug=True)
