import os, bs4, requests, argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('folder', help='The folder to download the files to')
	parser.add_argument('--url', '-u', required=True, help='The url to start scraping from')
	args = parser.parse_args()

	url = args.url
	visited = []
	visited.append(url)
	folder = args.folder
	
	os.makedirs(folder, exist_ok=True)
 	
	counter= 1
	print('Starting download...')
	looped = False
	while not looped:
		print('Downloading file %s...'%(url))
		res= requests.get(url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text)

		htmlFile = open(os.path.join(folder,str(counter)+ '. '+os.path.basename(url)), 'wb')
		counter = counter + 1
		for chunk in res.iter_content(100000):
			htmlFile.write(chunk)
		htmlFile.close()

		nextUrl = 'http://www.tutorialspoint.com'+soup.select('.nxt-btn a')[0].get('href')
		if nextUrl in visited:
			looped = True
		else:
			url = nextUrl
			visited.append(url)

	print('\nDone\n')

if __name__=='__main__':
	main()