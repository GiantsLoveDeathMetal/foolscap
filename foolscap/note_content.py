import os

from note_data import save_data
from parse_text import (
    load_text,
    edit_text,
    unique_heading,
    shift_lines,
    note_component,
    update_component,
)
from file_paths import NOTE_FOLDERS


def save_note(new_note, saved_notes, temp_file=False):
    """ Convert note.txt to dict components and save.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """

    if not temp_file:
        new_note = load_text(new_note)

    new_component = note_component(new_note)

    saved_notes.update(new_component)
    save_data(saved_notes)


def view_note(note, stored_data):
    """ Print the note to console if found.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    name_note = NOTE_FOLDERS['GET_NOTE']

    if note in stored_notes:
        note_text = load_text(name_note.format(note_name=note))

        for line in note_text:
            print(line)

    else:
        # Fuzzy here
        print('Not found')


def list_notes(tags, all_notes):
    # change template if more info is wanted
    # add config for changing list style
    # This should get data, cli face should order data.

    if tags is not None:
        all_notes = {
            key: values
            for key, values in all_notes.items()
            if 'tags' in values and tags in values['tags']
        }

    if len(all_notes) == 0:
        print("No note tagged with '{tag}'".format(tag=tags))

    basic_template = "+---> {title}\n"
    description_template = "   \\->  {description}\n"
    # tags_template = " --  {tags}\n"

    # Below for loop should move to cli.
    for key, values in all_notes.items():
        if 'description' in values:
            print(basic_template.format(title=key), end=' ')
            print(
                description_template.format(
                    description=values['description']
                )
            )

            # if 'tags' in values:
            # print tags_template.format(tags=(' '.join(values['tags'])))

        else:
            print(basic_template.format(title=key))


def delete_note(note, stored_data):
    """ Delete a note stored in foolscap

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()

    if note in stored_notes:
        delete_file = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        recycle_bin = unique_heading(note, folder='IN_BIN')

        os.rename(delete_file, recycle_bin)

        stored_data.pop(note, None)
        save_data(stored_data)

    else:
        # Fuzzy here
        print('Not found')


def edit_note(note, stored_data):
    """ Edit the note from data in vim.

    :param note: (string) name of .txt file.
    :param stored_data: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()

    if note in stored_notes:
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        edit_text(editing=edited_note)

        stored_data = update_component(note, stored_data)
        save_data(stored_data)

        print('Note updated')

    else:
        # Fuzzy here
        print('Not found')


def new_note(stored_notes):
    """ Create a new note in vim from template.

    :param stored_notes: (dict) of notes in data.
    """
    new_text = edit_text()

    # don't write unchanged notes.
    if '# title' != new_text[0]:
        save_note(new_text, stored_notes, temp_file=True)

    else:
        print('Aborted New Note')


def move_lines(note, stored_data):
    """ Move selected lines from a note to another note.

    :parma note: (string) title of note to move lines to.
    :param stored_data: (dict) of notes in data.
    """
    from_note = input('Move lines from? ')

    stored_notes = stored_data.keys()
    if note not in stored_notes:
        print('{} not found.'.format(note))

    if from_note in stored_notes:
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=from_note)
        edit_text(editing=edited_note)

        stored_data = shift_lines(from_note, note)
    else:
        print('{} not found.'.format(from_note))

