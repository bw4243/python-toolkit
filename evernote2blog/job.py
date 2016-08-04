#!/usr/bin/python
# -*-coding:utf-8-*-
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import *
from evernote.edam.type.ttypes import NoteSortOrder
from xml.etree import ElementTree


def syn_note2blog():
    developer_token = "S=s60:U=c44607:E=15cab210d07:C=155536fdd40:P=1cd:A=en-devtoken:V=2:H=62a11e1a5962a7aa6e456e01a02922e1"

    # Set up the NoteStore client
    client = EvernoteClient(token=developer_token, service_host='app.yinxiang.com')
    note_store = client.get_note_store()

    latestUpdateCount = 0
    currentState = note_store.getSyncState(developer_token)
    currentUpdateCount = currentState.updateCount

    if currentUpdateCount > latestUpdateCount:
        # TODO:get the latest notes
        latestUpdateCount = currentUpdateCount

        # Make API calls
        notebooks = note_store.listNotebooks()

        guid = [book.guid for book in notebooks if book.name == '博客'][0]

        print('博客 guid', guid)

        metadatalist = note_store.findNotesMetadata(developer_token,
                                                    NoteFilter(order=NoteSortOrder.CREATED, notebookGuid=guid,
                                                               ascending=False), 0, 10,
                                                    NotesMetadataResultSpec(includeTitle=True))
        for metadata in metadatalist.notes:
            print(metadata.title)
            note_content=note_store.getNoteContent(developer_token,metadata.guid)
            print(note_content)
            root = ElementTree.fromstring(note_content)
            print(root)





if __name__ == '__main__':
    syn_note2blog()
