"""
    merge:
        Add an input CSV file into a summary output file

    Usage:
        merge [options] <input_file> <summary_file>

    Options:
        --backup[=ext] Save a backup version of the original summary file, with the provided extension 
"""
import hepshell
import pandas as pd
from shutil import copyfile

# TODO: Implement run() method
# TODO: return True if successful
# TODO: text that should be printed / logged should be added to the Command object's __text attribute
# TODO: tidy up the docstring for this file

class Command(hepshell.Command):
    DEFAULTS = dict(
            backup="bak",
            #backup=None,
    )

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(**Command.DEFAULTS)
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        if len(args)!=2:
            self.__text="Error: merge command needs exactly 2 arguments"
            return False

        input_filename=args[0]
        summary_filename=args[1]
        save_backup=False

        to_add=pd.read_csv(input_filename)
        summary=pd.read_csv(summary_filename)

        if "backup" in variables:
            backup=variables["backup"]
            print(backup,type(backup))
            backup_name=summary_filename+"."+variables["backup"]
            copyfile(summary_filename,backup_name )

        summary=summary.append(to_add,ignore_index=True)
        summary.to_csv(summary_filename,index=False)
        return True
