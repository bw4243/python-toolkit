#!/usr/bin/python
# -*-coding:utf-8-*-
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import *
from evernote.edam.type.ttypes import NoteSortOrder


def syn_note2blog():
    developer_token = "S=s60:U=c44607:E=15cab210d07:C=155536fdd40:P=1cd:A=en-devtoken:V=2:H=62a11e1a5962a7aa6e456e01a02922e1"

    # Set up the NoteStore client
    client = EvernoteClient(token=developer_token, service_host='app.yinxiang.com')
    note_store = client.get_note_store()

    latestUpdateCount = 0
    currentState = note_store.getSyncState(developer_token)
    currentUpdateCount = currentState.getUpdateCount()

    if currentUpdateCount > latestUpdateCount:
        # TODO:get the latest notes
        latestUpdateCount = currentUpdateCount

        # Make API calls
        notebooks = note_store.listNotebooks()

        guid = [book.guid for book in notebooks if book.name == '博客'][0]

        print('博客 guid', guid)

        # note = Note()
        # note.title = "I'm a test note!"
        # note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        # note.content += '<en-note>Hello, world!</en-note>'
        # note = note_store.createNote(note)

        # note_store.getNote()

        metadatalist = note_store.findNotesMetadata(developer_token,
                                                    NoteFilter(order=NoteSortOrder.CREATED, notebookGuid=guid,
                                                               ascending=False), 0, 10,
                                                    NotesMetadataResultSpec(includeTitle=True))
        for metadata in metadatalist.notes:
            print(metadata.title)


if __name__ == '__main__':
    syn_note2blog()
