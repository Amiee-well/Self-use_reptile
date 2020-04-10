import os
import re
import time
import Tracks
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def getRightPositions(gt_cut_bg_slice, gt_cut_fullbg_slice):
	gap_image_loc_list = []
	full_image_loc_list = []
	for each in gt_cut_bg_slice:
		x, y = [int(i) for i in re.findall(r'background-position:\s(.*?)px\s(.*?)px;', each.get('style'))[0]]
		gap_image_loc_list.append([x, y])
	for each in gt_cut_fullbg_slice:
		x, y = [int(i) for i in re.findall(r'background-position:\s(.*?)px\s(.*?)px;', each.get('style'))[0]]
		full_image_loc_list.append([x, y])
	return gap_image_loc_list, full_image_loc_list

def reorganImage(image, positions):
	uppers = []
	downs = []
	for pos in positions:
		if pos[-1] == -58:
			uppers.append(image.crop((abs(pos[0]), 58, abs(pos[0])+10, 116)))
		else:
			downs.append(image.crop((abs(pos[0]), 0, abs(pos[0])+10, 58)))
	image_new = Image.new('RGB', image.size)
	offset = 0
	for each in uppers:
		image_new.paste(each, (offset, 0))
		offset += 10
	offset = 0
	for each in downs:
		image_new.paste(each, (offset, 58))
		offset += 10
	return image_new

def getGapOffset(image, source_img, thresh=150):
	for i in range(60, image.size[0]):
		for j in range(image.size[1]):
			pixel1 = image.getpixel((i, j))
			pixel2 = source_img.getpixel((i, j))
			if abs(pixel1[0]-pixel2[0]) + abs(pixel1[1]-pixel2[1]) + abs(pixel1[2]-pixel2[2]) >= thresh:
				return i

def moveToGap(browser, slider, tracks):
	ActionChains(browser).click_and_hold(slider).perform()
	for track in tracks:
		ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()
		time.sleep(0.01)
	ActionChains(browser).pause(0.5).release().perform()

def main(url):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--start-maximized')
	browser = webdriver.Chrome(
		executable_path = './driver/chromedriver.exe',
		options = chrome_options
		)
	browser.get(url)
	slider = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#gc-box > div > div.gt_slider > div.gt_slider_knob.gt_show")))
	username = browser.find_element_by_id("login-username")
	username.send_keys('18956436295')
	password = browser.find_element_by_id("login-passwd")
	password.send_keys('abcd123456')
	soup = BeautifulSoup(browser.page_source, 'lxml')
	gt_cut_bg_slice = soup.find_all(class_='gt_cut_bg_slice')
	gt_cut_fullbg_slice = soup.find_all(class_='gt_cut_fullbg_slice')
	gap_image_url = re.findall(r'background-image:\surl\("(.*?)"\)', gt_cut_bg_slice[0].get('style'))[0].replace('webp', 'jpg')
	full_image_url = re.findall(r'background-image:\surl\("(.*?)"\)', gt_cut_fullbg_slice[0].get('style'))[0].replace('webp', 'jpg')
	gap_image = Image.open(BytesIO(requests.get(gap_image_url).content))
	full_image = Image.open(BytesIO(requests.get(full_image_url).content))
	gap_image_loc_list, full_image_loc_list = getRightPositions(gt_cut_bg_slice, gt_cut_fullbg_slice)
	gap_image = reorganImage(gap_image, gap_image_loc_list)
	full_image = reorganImage(full_image, full_image_loc_list)
	gap_image.save('1.jpg')
	full_image.save('2.jpg')
	distance = getGapOffset(gap_image, full_image)
	tracks = Tracks.getTracks(int(distance*0.95), 12, 3)
	moveToGap(browser, slider, tracks)
	time.sleep(2)


if __name__ == '__main__':
	url = 'https://passport.bilibili.com/login'
	main(url)
