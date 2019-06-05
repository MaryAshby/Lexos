import json

import pandas as pd
from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager

word_cloud_blueprint = Blueprint("word_cloud", __name__)


@word_cloud_blueprint.route("/word-cloud", methods=["GET"])
def word_cloud() -> str:
    """ Gets the word cloud page.

    :return: The word cloud page.
    """

    # Set the cloud options to their defaults if they do not exist
    if "cloudoption" not in session:
        session["cloudoption"] = constants.DEFAULT_CLOUD_OPTIONS

    return render_template("word-cloud.html")


@word_cloud_blueprint.route("/word-cloud/get-word-counts", methods=["GET"])
def get_word_counts() -> str:
    """ Gets the top 100 word counts across all active files.

    :return: The top 100 word counts across all active files.
    """

    file_manager = utility.load_file_manager()
    session_manager.cache_cloud_option()

    # Get the contents of the active documents
    contents = ""
    for file in file_manager.files.values():
        if file.active:
            contents += file.load_contents()

    # If there are no active documents or contents, return an empty array
    if not contents:
        return "[]"

    # Get a sorted dataframe of word counts
    dtm, words = utility.simple_vectorizer([contents], "word", 1)
    dataframe = pd.DataFrame({"word": words, "count": dtm[0]})
    dataframe = dataframe.sort_values(by="count", ascending=False)

    # Create a list of the top 100 words and their normalized counts
    response = []
    maximum = dataframe.iloc[0]["count"]
    dataframe = dataframe[:100]
    for i in range(len(dataframe)):
        response.append([dataframe.iloc[i]["word"],
                         dataframe.iloc[i]["count"]/maximum])
    return json.dumps(response)
