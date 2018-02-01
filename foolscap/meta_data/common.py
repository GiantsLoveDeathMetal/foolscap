from datetime import datetime

from foolscap.file_paths import NOTE_FOLDERS

from foolscap.meta_data.io import load_meta
from foolscap.meta_data.io import save_meta
from foolscap.meta_data.utils import fuzzy_guess
from foolscap.meta_data.parse_note import (


)


def note_exists(note):
    stored_notes = load_meta.keys()
    if note in stored_notes:
        return True
    else:
        fuzzy_guess(note, stored_notes)


def remove_component(note):
    stored_notes = load_meta.keys()
    stored_notes.pop(note, None)
    save_meta(stored_notes)


def add_component(component):
    stored_notes = load_meta()
    stored_notes.update(component)


def update_component(note):
    stored_notes = load_meta.keys()

    note_name = NOTE_FOLDERS['GET_NOTE'].format(
        note_name=note
    )
    note_edited = load_text(note_name)

    new_name = restrict_title(get_title(note_edited)[0])
    new_content = get_contents(note_edited)[0]

    if new_name != note and new_name in stored_notes:
        print('Warning!: Edited note title already exists!')
        new_name = unique_heading(new_name)

    # Note name has been changed, update the meta_data hook.
    if new_name != note and new_name not in stored_notes:
        stored_data[new_name] = stored_data[note]
        stored_data.pop(note, None)

    os.remove(note_name)
    save_text(new_name, new_content)

    stored_data[new_name]['modified'] = datetime.now()
    stored_data[new_name]['views'] += 1

    description = note_description(new_content)
    if description:
        stored_data[new_name]['description'] = description

    tags = note_tags(new_content)
    if tags:
        stored_data[new_name]['tags'] = tags

    save_data(stored_data)


def new_component(text):
    """ Creates the new note data structure.
        Here is where one would add more note information.

    :param list[str] note: containing a single note.
    :return: the dict note element.
    """
    # Text should be a string.
    # Passing to parse text should return basic components.
    # This function should then append components not found in note
    titles = get_title(text)
    contents = get_contents(text)

    # This loops through multiple notes
    note_component = {}
    for note_title, content in zip(titles, contents):
        note_title = restrict_title(text)
        title = unique_heading(note_title)

        note_component[title] = {'created': datetime.now()}
        note_component[title]['views'] = 1
        note_component[title]['modified'] = datetime.now()

        description = note_description(content)
        if description:
            note_component[title]['description'] = description

        tags = note_tags(content)
        if tags:
            note_component[title]['tags'] = tags

        sub_headings = parse_sub_headings(content)
        if sub_headings:
            note_component[title]['sub_headings'] = sub_headings

    add_component(note_component)
    return titles, contents