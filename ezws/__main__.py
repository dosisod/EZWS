from ezws.ezws import EZWS

def main() -> None:
	ez=EZWS("config.json", "bot")
	ez.grab()
	print(ez.data)

if __name__=="__main__":
	main()