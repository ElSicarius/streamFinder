
import argparse


def get_arguments():
    """
    Parses the argparse object
    :returns the arguments object
    """
    parser = argparse.ArgumentParser(description='', epilog="")
    parser.add_argument('title', help='Movie title', default=None)

    parser.add_argument('-l',"--lang", help='language of the streaming', default="vf")

    parser.add_argument("-s", "--sources", help="select sources for streaming; values -> see readme (google is shit, recommended:\"DE\")", default="DE")

    parser.add_argument("-n", "--numberResults", help="number of results from differents search engines", default=30)
    args = parser.parse_args()
    return args
