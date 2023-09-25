from os import walk

def get_tree(directory):
	dirs = [x[0] for x in walk(directory)]
	print(dirs)

if __name__ == '__main__':
	get_tree("test")