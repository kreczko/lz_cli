"""
    merge:
        Add an input CSV file into a summary output file

    Usage:
        merge [options] <input_file>[ <input_file2>[...]] <summary_file>

    Options:
        --append       Instead of overwriting the summary file, append the input data to it
"""
import hepshell
import pandas as pd

class Command(hepshell.Command):
    DEFAULTS = dict(
    )

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(**Command.DEFAULTS)
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args,variables)
        if len(self.__args)<2:
            self.__text="Error: merge command needs at least 2 arguments"
            return False

        input_filenames=args[:-1]
        summary_filename=args[-1]

        if self.__variables.get("append",False) is True:
            input_filenames=[summary_filename]+input_filenames

        summary=None
        for input_file in input_filenames:
            to_add=pd.read_csv(input_file)
            if summary is None:
                summary=to_add
            else:
                summary=summary.append(to_add,ignore_index=True)

        summary.to_csv(summary_filename,index=False)
        return True
