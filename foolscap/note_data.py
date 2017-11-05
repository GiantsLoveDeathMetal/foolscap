import os
import pickle


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_STORAGE = os.path.join('data', 'note_data.pkl')
REAL_DATA = os.path.join(SCRIPT_DIR, DATA_STORAGE)

# Write example data:
def save_data(data):
    """:param data: (dict) containing all notes."""
    with open(REAL_DATA, 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def note_data():
    """ Load the note data into a dict."""
    try:
        with open(REAL_DATA, 'rb') as _input:
            return pickle.load(_input)

    except EOFError and IOError:
        return {}

