import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--npz", type=str)
	args = parser.parse_args()

	if args.npz == None:
		print("No argments")
	else:
		print(args.npz)

if __name__ == '__main__':
	main()

