import os
import pickle

from flask import session, request

import helpers.constants as constants

def session_folder():
    return os.path.join(constants.UPLOAD_FOLDER, session['id'])

def init():
    """
    Initializes a new session.

    *Called in reset() (when 'reset' button is clicked).

    Args:
        None

    Returns:
        Redirects to upload() with a "GET" request.
    """
    import random, string
    from models.ModelClasses import FileManager

    folderCreated = False
    while not folderCreated: # Continue to try to make
        try:
            session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
            print 'Attempting new id of', session['id'], '...',
            os.makedirs(session_folder())
            folderCreated = True
            print 'Good.'

        except: # This except block will be hit if and only if the os.makedirs line throws an exception
            print 'Already in use.'

    emptyFileManager = FileManager(session_folder())
    dumpFileManager(emptyFileManager)

    print 'Initialized new session, session folder, and empty file manager with id.'


def loadFileManager():
    from models.ModelClasses import FileManager

    managerFilePath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    fileManager = pickle.load(open(managerFilePath, 'rb'))
    
    return fileManager


def dumpFileManager(fileManager):
    from models.ModelClasses import FileManager
    
    managerFilePath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    pickle.dump(fileManager, open(managerFilePath, 'wb'))

def cacheAlterationFiles():
    for uploadFile in request.files:
        fileName = request.files[uploadFile].filename
        if fileName != '':
            session['scrubbingoptions']['optuploadnames'][uploadFile] = fileName
    session.modified = True # Necessary to tell Flask that the mutable object (dict) has changed


def cacheScrubOptions():
    """
    Stores all scrubbing options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for box in constants.SCRUBBOXES:
        session['scrubbingoptions'][box] = (box in request.form)
    for box in constants.TEXTAREAS:
        session['scrubbingoptions'][box] = (request.form[box] if box in request.form else '')
    if 'tags' in request.form:
        session['scrubbingoptions']['keepDOEtags'] = request.form['tags'] == 'keep'
    session['scrubbingoptions']['entityrules'] = request.form['entityrules']


def cacheCuttingOptions():
    """
    Stores all cutting options in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    if request.form['cut_type'] == 'size':
        legendCutType = 'size'
        lastProp = request.form['lastprop']
    else:
        legendCutType = 'number'
        lastProp = '50%'

    session['cuttingoptions'] = {'cut_type': legendCutType,
                                 'cutting_value': request.form['cutting_value'],
                                 'overlap': request.form['overlap'],
                                 'lastprop': lastProp}

def cacheCSVOptions():
    """
    Stores all CSV options in the session cookie object.

    Args:
        None

    Returns:
        None
    """

    session['csvoptions'] = {'csvdata': request.form['csvdata'],
                             'csvorientation': request.form['csvorientation'],
                             'csvdelimiter': request.form['csvdelimiter']}