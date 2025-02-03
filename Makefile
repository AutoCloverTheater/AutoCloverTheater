mac:
	pyinstaller --onefile --windowed --add-data "img:img"  --name MyApp_mac ./src/app/main.py