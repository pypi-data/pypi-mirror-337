import random, subprocess

class DeviceCatalog:
	
	def generate_model(Jar):
		return {
			"Realme": ["Realme 12 Pro", "Realme GT Neo 6", "Realme C67", "Realme Narzo 60","Realme 10 Pro+", "Realme GT 5", "Realme 9i", "Realme C55", "Realme Narzo 50","Realme 8 Pro", "Realme X7 Max", "Realme C35", "Realme Narzo 30", "Realme GT Neo 5","Realme GT 2 Pro", "Realme 7", "Realme X50 Pro", "Realme C25s", "Realme 6 Pro"],
			"Samsung": ["SM-A135F","Galaxy S23 FE", "Galaxy A34", "Galaxy Z Flip5", "Galaxy M14 5G", "Galaxy S22","Galaxy A14", "Galaxy M13", "Galaxy F23 5G", "Galaxy Z Fold4", "Galaxy S21 Ultra","Galaxy Note 20 Ultra", "Galaxy A73", "Galaxy Xcover 6 Pro", "Galaxy S20 FE","Galaxy A52s 5G","SM-A135F", "Galaxy S24 Ultra", "Galaxy Z Fold5", "Galaxy A54", "Galaxy M14"],
			"Oppo": ["CPH2591","CPH2591", "Oppo Find X7 Pro", "Oppo Reno 11", "Oppo A98", "Oppo K11","Oppo Find N3 Flip", "Oppo A78", "Oppo F23", "Oppo Reno 8T", "Oppo Reno 7","Oppo K10", "Oppo A58", "Oppo Find X5 Pro", "Oppo Reno 6 Pro", "Oppo A17","Oppo Find X3 Pro", "Oppo A55", "Oppo F19 Pro", "Oppo Reno 5", "Oppo A16K"],
			"Vivo": ["Vivo X100 Pro", "Vivo V30", "Vivo Y200", "Vivo T2 5G","Vivo X100 Pro", "Vivo V30", "Vivo Y200", "Vivo T2 5G", "Vivo X90s","Vivo iQOO 12", "Vivo Y78", "Vivo V27", "Vivo Y16", "Vivo iQOO Neo 7","Vivo X80 Pro", "Vivo Y33s", "Vivo V25 Pro", "Vivo Y21", "Vivo X70 Pro+","Vivo V21", "Vivo Y12s", "Vivo T1 5G", "Vivo X60", "Vivo iQOO 9 Pro"],
			"Huawei": ["Huawei P70 Pro", "Huawei Mate 60", "Huawei Nova 12", "Huawei Enjoy 70","Huawei P70 Pro", "Huawei Mate 60", "Huawei Nova 12", "Huawei Enjoy 70","Huawei P60", "Huawei Mate X5", "Huawei Y9a", "Huawei Nova 11i", "Huawei P50 Pocket","Huawei Mate 50 Pro", "Huawei P40", "Huawei Y7a", "Huawei Nova 9", "Huawei Mate X3","Huawei P30 Pro", "Huawei Y6p", "Huawei Mate 40", "Huawei Nova 7", "Huawei Enjoy 20"],
			"Google": ["Pixel 9 Pro", "Pixel 8a", "Pixel 7", "Pixel Fold 2","Pixel 9 Pro", "Pixel 8a", "Pixel 7", "Pixel Fold 2", "Pixel 6a","Pixel Tablet", "Pixel 5", "Pixel 4a", "Pixel 3 XL", "Pixel 2 XL","Pixel 6 Pro", "Pixel 5a", "Pixel 4", "Pixel 3a", "Pixel Slate"],
			"Xiaomi": ["23053RN02A", "22111317PG","23053RN02A", "22111317PG", "Xiaomi 14 Ultra", "Redmi Note 13 Pro", "Poco F5","Black Shark 5 Pro", "Xiaomi 13T Pro", "Redmi K60", "Poco X5 Pro", "Xiaomi Pad 6","Xiaomi Mi 11 Ultra", "Redmi Note 12", "Poco F4 GT", "Black Shark 4", "Redmi 10C","Xiaomi 12 Pro", "Poco M4 Pro", "Xiaomi Mi Mix Fold", "Redmi K40", "Xiaomi Mi 10T Pro"],
			"OnePlus": ["OnePlus 12", "OnePlus 11R", "OnePlus Nord 3", "OnePlus 10 Pro", "OnePlus Ace 2","OnePlus 9 Pro", "OnePlus 8T", "OnePlus Nord CE 2", "OnePlus 7T", "OnePlus 6"],
			"Sony": ["Xperia 1 V", "Xperia 5 V", "Xperia 10 IV", "Xperia Pro-I","Xperia 1 III", "Xperia 5 III", "Xperia 10 III", "Xperia XZ2", "Xperia Z5"],
			"Motorola": ["Moto G84", "Moto Edge 40", "Moto Razr 40 Ultra", "Moto G73","Moto G200", "Moto Edge 30 Pro", "Moto G60", "Moto Razr 2022", "Moto G100"],
			"Nothing": ["Nothing Phone (2)", "Nothing Phone (1)"],
			"Asus": ["ROG Phone 8", "Zenfone 10", "ROG Phone 7", "Zenfone 9", "ROG Phone 6D"],
			"Lenovo": ["Lenovo Legion Phone Duel 2", "Lenovo Tab P12 Pro", "Lenovo K13", "Lenovo Z6 Pro"],
			"Nokia": ["Nokia X30 5G", "Nokia G60", "Nokia C32", "Nokia XR20", "Nokia 5.4"],
			"ZTE": ["ZTE Axon 50 Ultra", "ZTE Nubia Red Magic 8 Pro", "ZTE Blade V40", "ZTE Axon 40 Ultra"],
			"Honor": ["Honor Magic6 Pro", "Honor 90", "Honor X50", "Honor Play 40", "Honor Magic5 Ultimate"],
			"Meizu": ["Meizu 20 Pro", "Meizu 18s", "Meizu 16T", "Meizu M10", "Meizu 15 Plus"],
			"Infinix": ["Infinix Zero 30", "Infinix Note 30", "Infinix Smart 8", "Infinix GT 10 Pro"],
			"Tecno": ["Tecno Phantom X2 Pro", "Tecno Camon 20", "Tecno Pova 5 Pro", "Tecno Spark 10"],
		}
	
	def generate_model_instagram(Jar):
		return {
			"samsung": ['SM-A045M', 'SM-A045F', 'SM-A045F', 'SM-A042F', 'SM-A042M', 'SM-A042F', 'SM-A047F', 'SM-A047F', 'SM-A105FN', 'SM-A105FN', 'SM-A105G', 'SM-A105M', 'U', 'SM-S102DL', 'SM-A102U', 'SM-A102U', 'SM-A102U1', 'SM-A107M', 'SM-A107F', 'SM-A107F', 'SM-A115F', 'SM-S115DL', 'SM-A115M', 'SM-A115F', 'SM-A125F', 'SM-A127F', 'SM-A125U', 'SM-A137F', 'SM-A135F', 'SM-A135U1', 'SAMSUNG SM-A135F', 'SM-A137F'],
			'OPPO': ['CPH1989', 'CPH1951', 'CPH1945', 'CPH1945', 'CPH2043', 'CPH2043', 'PDCM00', 'A001OP', 'PDCM00', 'PDCM00', 'PCRT01', 'PCRT01', 'CPH2009', 'CPH2035', 'CPH2037', 'CPH2013', 'A002OP', 'CPH2113', 'CPH2091', 'PDPM00', 'PDPT00', 'CPH2125', 'CPH2109', 'CPH2109', 'PDNM00', 'CPH2089', 'PDNM00', 'PDNT00', 'PEAT00', 'PEAM00', 'PEAM00', 'CPH2209', 'CPH2065', 'CPH2159', 'CPH2159', 'CPH2145', 'PEGM00', 'CPH2205', 'CPH2207', 'PDSM00', 'CPH2201', 'PDST00', 'PDSM00', 'PDRM00'],
			'vivo': ['V2136A', 'V2136A', 'V2141A', 'V2171A', 'I2017', 'V2172A', 'V2172A', 'I2022', 'I2019', 'I2019', 'I2201', 'V1914A', 'V1914A', 'V1981A', 'V2055A', 'V2118A', 'V2157A', 'V2157A', 'V2154A', 'V2196A', 'V2196A', 'V2199A', 'V2231A', 'V2238A', 'V1936AL', 'V1936A', 'V1922A', 'V1922A', 'V1922A ', 'V1916A', 'V2023A', 'V2023A', 'VIVO V2023A', 'V2065A', 'V2061A', 'V2061A', 'V2143A', 'V2106A', 'V2165A', 'V2165A', 'V2180GA', 'V1986A', 'V2012A', 'V2012A', 'V2073A', 'V2073A', 'I2011', 'V2148A', 'I2018', 'V1919A'],
			'Xiaomi': ['Xiaomi 10 Pro', '2107119DC', '2107119DC', '21091116UI', '21091116UI', '2201123G', '2201123C', 'Xiaomi 12', '2203129G', 'Xiaomi 12 Lite', '2201122G', 'Xiaomi 12 Pro', '2207122MC', '2207122MC', '2206123SC', '2206122SC', 'Xiaomi 12S Pro', '2206122SC', '2203121C', '2203121C', '2203121C', '22071212AG', 'Xiaomi 12T', 'Xiaomi 12T Pro', '22081212UG', 'Xiaomi 12T Pro', '2112123AG', '2211133G', '2211133C', 'Xiaomi 13', 'Xiaomi 13', 'Xiaomi 13', '2210129SG', 'Xiaomi 13 Lite', 'Xiaomi 13 Lite', 'Xiaomi 13 Lite', 'Xiaomi 13 Lite', '2210132C', 'Xiaomi 13 Pro', '2210132G', 'Xiaomi 13 Pro', '2210132C', 'xiaomi 6', 'xiaomi 6', 'xiaomi 8'],
			'HUAWEI': ['PCT-AL10', 'ALA-AN70', 'KNT-AL10', 'KNT-AL20', 'KNT-AL20', 'KNT-UL10', 'KNT-TL10', 'DUK-AL20', 'DUK-AL20', 'DUK-AL20', 'JMM-AL00', 'JMM-AL10', 'JMM-TL10', 'JMM-AL00', 'BKL-L04', 'PCT-L29', 'OXF-AN00', 'OXF-AN00', 'OXF-AN00', 'OXF-AN00', 'OXF-AN00', 'OXF-AN00', 'OXF-AN00', 'OXF-AN10', 'OXF-AN10', 'TEL-AN00a', 'TEL-AN00a', 'TEL-AN00a', 'TEL-AN00a', 'TEL-AN00', 'TEL-AN00a', 'TEL-AN10', 'TEL-AN00a', 'TEL-AN00a', 'TEL-TN00', 'TEL-AN10', 'Honor X10 Lite', 'DNN-LX9', 'KKG-AN00', 'KKG-AN00', 'KKG-AN00', 'KKG-AN00', 'KKG-AN00', 'Honor X10 Max', 'Honor X10 Pro', 'KKG-AN70', 'TFY-AN00', 'ADT-AN00'],
			'HTC/htc': ['HTC_D516', 'HTC-D516d', 'HTC D516d', 'HTC D516t', 'HTC D516w', 'HTC_D516w', 'HTC_D530u', 'HTC D539', 'HTC D610', 'HTC_D610', 'HTC D610t', 'HTC_D610t', 'HTC D616w', 'HTC_D616w', 'HTC_D620u', 'HTC D626', 'HTC D626d', 'HTC_D626h', 'HTC_D626q', 'HTC D626t', 'HTC_D626t', 'HTC D626w', 'HTC_D626w', 'HTC_D626x', 'HTC D628h', 'HTC_D628u', 'HTC_D630x', 'HTC_D650h', 'HTC D728', 'HTC D728w', 'HTC_D728x', 'HTC D816', 'HTC D816d', 'HTC D816e', 'HTC_D816e', 'HTC D816t', 'HTC_D816t', 'HTC D816v', 'HTC D816w', 'HTC_D816W', 'HTC_D816w', 'HTC D820', 'HTC_D820f', 'HTC_D820G', 'vi HTC_D820m'],
			'Realme': ['RMX3686', 'RMX3687', 'RMX3687', 'RMX1805', 'RMX1809', 'RMX1805', 'RMX1801', 'RMX1807', 'RMX1821', 'RMX1825', 'RMX1851', 'RMX1827', 'RMX1911', 'RMX1971', 'RMX2030', 'RMX1925', 'RMX2001', 'RMX2061', 'RMX2040', 'RMX2002', 'RMX2151', 'RMX2155', 'RMX2170', 'RMX2103', 'RMX3085', 'RMX3241', 'RMX3081', 'RMX3151', 'RMX3381', 'RMX3521', 'RMX3388', 'RMX3474', 'RMX3474', 'RMX3472', 'RMX3471', 'RMX3393', 'RMX3392', 'RMX3491', 'RMX3612', 'RMX1811', 'RMX2185', 'RMX2185', 'RMX3231', 'RMX2189', 'RMX2180', 'RMX2195', 'RMX2101', 'RMX2101', 'RMX1941', 'RMX1941', 'RMX1945', 'RMX1945', 'RMX3063', 'RMX3061', 'RMX3201', 'RMX3261', 'RMX3263', 'RMX3191', 'RMX3193', 'RMX3195', 'RMX3197', 'RMX3269', 'RMX3268', 'RMX2020']
		}

class GenerateUseragent:
	
	os_ver = {'9': 'PPR1', '10': 'QP1A', '11': 'RP1A', '12': 'SP1A', '13': 'TP1A', '14': 'UP1A'}
	
	def __init__(Jar):
		Jar.brand_face = DeviceCatalog().generate_model()
		Jar.model_list_face = list(Jar.brand_face.keys())
		Jar.brand_insta = DeviceCatalog().generate_model_instagram()
		Jar.model_list_insta = list(Jar.brand_insta.keys())
		Jar.dpi_pixel = random.choice(['240dpi; 1760x792', '240dpi; 1920x864', '320dpi; 2400x1080','400dpi; 3200x1440', '480dpi; 1080x1920', '320dpi; 900x1600','320dpi; 720x1280', '240dpi; 540x960', '280dpi; 1920x1080','240dpi; 160x900', '240dpi; 1280x720', '160dpi; 960x540'])
    
	
	def android_version_instagram(Jar, android_version):
		version_map = {'9': '28', '10': '29', '11': '30', '12': '31', '13': '32', '14': '33'}
		return version_map.get(str(android_version), '34')
        
	def versi_chrome(Jar):
		return f'{random.randrange(100, 133)}.0.{random.randrange(4200, 6900)}.{random.randrange(40, 190)}'
		
	def android_version(Jar, android_version):
		return Jar.os_ver.get(str(android_version), 'AP4A')
	
	def get_device_instagram(Jar, brand=None, system=False):
		if system:return Jar.get_system_device_insta()
		if not brand or brand not in Jar.brand_insta:
			brand = random.choice(Jar.model_list_insta)
		model = random.choice(Jar.brand_insta[brand])
		android = random.choice(['9', '10', '11', '12', '13', '14', '15'])
		sdk = Jar.android_version_instagram(android)
		return {'brand': brand, 'model': model, 'hardware': 'marlin; qcom', 'android': android, 'sdk': sdk}
	
	def get_device_chrome(Jar, brand=None, system=False):
		if system:return Jar.get_system_device_ch()
		if not brand or brand not in Jar.brand_face:
			brand = random.choice(Jar.model_list_face)
		model = random.choice(Jar.brand_face[brand])
		android = random.choice(['9', '10', '11', '12', '13', '14', '15'])
		build_code = Jar.android_version(android)
		build =f"{build_code}.{random.randint(211111, 233333)}.00{random.randint(1, 9)}"
		return {"model": model, 'android': android, 'chrome': Jar.versi_chrome(), 'build': build}
	
	def get_system_device_insta(Jar):
		try:
			brand = subprocess.check_output("getprop ro.product.manufacturer", shell=True).decode().strip()
			model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
			hardware = subprocess.check_output("getprop ro.hardware", shell=True).decode().strip()
			android = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip()
			sdk = subprocess.check_output("getprop ro.build.version.sdk", shell=True).decode().strip()
			if not brand or not model or not android:
				Jar.get_device_instagram()
			return {'brand': brand,'model': model,'hardware': hardware,'android': android,'sdk': sdk}
		except Exception:
			Jar.get_device_instagram()
			
	def get_system_device_ch(Jar):
		try:
			model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
			android = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip()
			build = subprocess.check_output("getprop ro.product.build.id", shell=True).decode().strip()
			if not model or not android or not build:
				Jar.get_device_chrome()
			return {"model": model, 'android': android, 'chrome': Jar.versi_chrome(), 'build': build}
		except Exception:
			Jar.get_device_chrome()
	
	def get_device_face(Jar, brand=None, system=False):
		if system:return Jar.get_system_face()
		if not brand or brand not in Jar.brand_face:
			brand = random.choice(Jar.model_list_face)
		model = random.choice(Jar.brand_face[brand])
		android = random.choice(['9', '10', '11', '12', '13', '14', '15'])
		simcard = random.choice(['Telkomsel', 'XL Axiata', 'Indosat', 'Smartfren', 'Tri'])
		return {'brand': brand, 'brand2': brand,'model': model, 'android': android, 'cpu': 'arm64-v8a', 'simcard': simcard}
	
	def get_system_face(Jar):
		try:
			brand = subprocess.check_output("getprop ro.product.manufacturer", shell=True).decode().strip()
			brand2 = subprocess.check_output("getprop ro.product.brand", shell=True).decode().strip()
			model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
			android = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip()
			simcard = subprocess.check_output('getprop gsm.operator.alpha', shell=True).decode().strip().split(",")[1].replace("\n","")
			cpu = subprocess.check_output("getprop ro.product.cpu.abi", shell=True).decode().strip()
			if not model or not android or not cpu:
				Jar.get_device_face()
			return {'brand': brand, 'brand2': brand2, 'model': model, 'android': android, 'cpu': cpu, 'simcard': simcard}
		except Exception:
			Jar.get_device_face()
	
	def chromeuseragent(Jar, brand=None, system=False):
		device_info = Jar.get_device_chrome(brand, system)
		model, android, chrome, build = device_info.values()
		return f'Mozilla/5.0 (Linux; Android {android}; {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Mobile Safari/537.36'
	
	def facebookuseragent(Jar, brand=None, system=False):
		density, width, height = round(random.uniform(1.0, 4.0), 2), random.randint(720, 1440), random.randint(1280, 2560)
		device_info = Jar.get_device_face(brand, system)
		brand, brand2, model, android, cpu, simcard = device_info.values()
		return f'[FBAN/FB4A;FBAV/486.0.0.66.70;FBBV/653066364;FBDM/{{density={density},width={width},height={height}}};FBLC/id_ID;FBRV/0;FBCR/{simcard};FBMF/{brand};FBBD/{brand2};FBPN/com.facebook.katana;FBDV/{model};FBSV/{android};FBOP/1;FBCA/{cpu}:;]'
	
	def instagramuseragent(Jar, brand=None, system=False):
		device_info = Jar.get_device_instagram(brand, system)
		brand, model, hardware, android, sdk = device_info.values()
		return f'Instagram 368.0.0.45.96 Android ({sdk}/{android}; {Jar.dpi_pixel}; {brand}; {model}; {hardware}; in_ID; 700073482)'