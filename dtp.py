from ftplib import FTP
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

	print(f"List of dirs: {dirs}")
	print(f"tree generated: {tree}")
	return (dirs, tree)

def send_dir(host, username, password, port, target, directory):
	print(f"Connecting to {host}")

	ftp = FTP(host)
	structure = get_tree(directory)
	paths = structure[0]

	ftp.login(username, password)

	# use top directory as parent directory
	parent = paths[0]
	# recreate paths without the parent
	paths = paths[1:]

	for path in paths:
		# remove parent from path (remove first occurance only because a sub directory may contain substring that matches parent)
		path = path.replace(parent + '/', "", 1)
		print(path)
		create_dirs(path, target, ftp, parent)

	ftp.quit()

def create_dirs(path, target, ftp, parent):
	# Adding / for better pathing
    if(target[-1] != '/'):
        target += '/'
    if(target[0] == '/'):
    	target = target[1:]

    print(f"cd to {target}")
    ftp.cwd(target)
    print(f"inside {ftp.pwd()}")

    if(parent):
    	# make parent dir
    	print(parent)
    	ftp.mkd(parent)
    	print(f"cd into parent: {parent}")

    parent = False


    if('/' in path):
        current_dir = path[:path.index('/')]
        next_dir = path[path.index('/') + 1:]
        print(f"Making directory {current_dir}")
        ftp.mkd(current_dir)
        target += current_dir + '/'
        ftp.cwd(current_dir)
        create_dirs(next_dir, target, ftp, parent)
    else: 
        print(f"Making final directory {path}")
        ftp.mkd(path)
        return 0

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog="DTP A simple solution for sending directories over ftp",
		description="Recursively send files from directory to ftp server conserving the original tree",
		epilog="Made by scaredontfear: sc4r3d0ntf34r@tuta.io"
		)

	parser.add_argument("host", help="The host to connect to.")
	parser.add_argument("-d", "--directory", help="The directory to send.")
	parser.add_argument("-t", "--target", help="Target directory to send files to (defaults to root directory).", default="/")
	parser.add_argument("-u", "--username", help="the username to connect to the ftp server")
	parser.add_argument("-P", "--password", help="The password to connect to the ftp server")
	parser.add_argument("-A", "--anon", help="Login anonymously to ftp server", action="store_true")
	parser.add_argument("-p", "--port", help="The port to connect to (defaults to 21).", default=21)

	args = parser.parse_args()

	if(not args.host):
		parser.print_help()
		print("No host specified exiting...")
		exit(6)
	else: 
		host = args.host

	if(not args.directory):
		print("please specify a directory.")
		parser.print_help()
		exit(4)
	if(not path.isdir(args.directory)):
		print("Directory invalid exiting...")
		exit(2)
	else:
		directory = args.directory

	if(args.anon):
		print("Logging in as anonymous user.")
		username = "anonymous"
		password=""
	elif(args.username):
		print(f"logging in as {args.username}")
		username = args.username
		if(args.password):
			password = args.password
		else:
			parser.print_help()
			print("Please specify password")
			exit(5)
	else:
		print("No user specified exiting...")
		exit(3)

	port = args.port
	target = args.target

	send_dir(host, username, password, port, target, directory)



