import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from bluer_objects import NAME
from bluer_objects import storage
from bluer_objects.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="download | upload",
)
parser.add_argument(
    "--object_name",
    type=str,
)
parser.add_argument(
    "--filename",
    type=str,
    default="",
)
args = parser.parse_args()


success = False
if args.task == "download":
    success = storage.download(
        object_name=args.object_name,
        filename=args.filename,
    )
elif args.task == "upload":
    success = storage.upload(
        object_name=args.object_name,
        filename=args.filename,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
