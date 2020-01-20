# run.py

from app.constants import APP, cache
from orm import setup

if __name__ == '__main__':
    setup()
    cache.init_app(APP)
    APP.run(debug=True, host='0.0.0.0')  # Do not write code after this point
