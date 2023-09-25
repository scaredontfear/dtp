import argparse
from os import walk
from os import path

def get_tree(directory):
	# returns dirs
	dirs = [x[0] for x in walk(directory)]
	# returns a list of lists of files in each subdir
	files_iter = [x[2] for x in walk(directory)]

	tree = list()
	# loop to create tree
	for d, f in zip(dirs, files_iter):
		for file in f:
			tree.append(f"{d}/{file}")

	return (dirs, tree)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog="DTP A simple solution for sending directories over ftp",
		description="Recursively send files from directory to ftp server conserving the original tree",
		epilog="Made by scaredontfear: sc4r3d0ntf34r@tuta.io"
		)

	parser.add_argument("-D", "--dir", help="The directory to send.")

	args = parser.parse_args()

	if(not path.isdir(args.dir)):
		print("Directory invalid exiting...")
		exit(2)

	structure = get_tree(args.dir)

	print(structure)