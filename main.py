from ezws import EZWS

def main():
	ez=EZWS("config.json", "bot")
	ez.grab()

if __name__=="__main__":
	main()
