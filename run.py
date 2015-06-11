#!flask/bin/python
import views

if __name__ == "__main__":
    views.app.run(debug=True, host="0.0.0.0")
