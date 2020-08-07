import requests
def check_internet():
	url='https://www.example.com/'
	timeout=3
	try:
		_ = requests.get(url, timeout=timeout)
		print("Internet True")
		return True
	except requests.ConnectionError:
		print("Internet False")
		return False

if __name__ == '__main__':
        check_internet()
