from __future__ import print_function
import basc_py4chan
import pandas as pd
import os
import time
import copy
import sys



def crawl(filename, board_name, lines):
    """ Crawl Function """
    while True:
        try:

            list_id = []
            #read in the current csv to ensure we dont have repeats
            if os.path.isfile(filename):
                list_id = pd.read_csv(filename)["post_id"].to_list()
            

            col_names = ["text_comment", "datetime", "post_id"]
            df = pd.DataFrame(columns = col_names)

            # get the board we want
            board = basc_py4chan.Board(board_name)

            # select the first thread on the board
            all_thread_ids = board.get_all_thread_ids()

            for thread_id in all_thread_ids:
                first_thread_id = thread_id
                thread = board.get_thread(first_thread_id)

                #check if empty thread
                if thread == None:
                    continue

                topic = thread.topic

                for thread in thread.all_posts:
                    if any(s.lower() in thread.comment.lower() for s in lines) and thread.post_id not in list_id:
                        temp_dict = {}
                        temp_dict["text_comment"] = thread.text_comment
                        temp_dict["datetime"] = thread.datetime
                        temp_dict["post_id"] = thread.post_id
                        df = df.append(temp_dict, ignore_index = True)

            if not os.path.isfile(filename):
                df.to_csv(filename, header='column_names')

            else: # else it exists so append without writing the header
                df.to_csv(filename, mode='a', header=False)
        except A:
            print(A)
            break



def main():
    """ Main function """

    # Read input
    filename = sys.argv[1].lower()
    board_name = sys.argv[2].lower()
    list_lines = sys.argv[3].lower()
    text_file = open(list_lines, "r")
    lines = text_file.read().strip('\n').split(',')
    results = crawl(filename, board_name, lines)




if __name__ == "__main__":
    main()

