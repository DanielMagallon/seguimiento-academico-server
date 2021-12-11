from src import *
from API import *


if __name__ == '__main__':
    print("Running flask server")
    # host_vb='192.168.122.1'
    # host_wl = '192.168.1.71'
    global_host = '0.0.0.0'
    app.run(debug=True, port='5800', host=global_host)
