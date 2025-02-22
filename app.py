import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import streamlit.components.v1 as components
import json
import requests


models = {'TRIUMPH': ('BONNEVILLE SE', 'BONNEVILLE T100', 'Bonneville Bobber Black', 'Bonneville Speedmaster', 'DAYTONA 600', 'DAYTONA 650', 'DAYTONA 675 TRIPLE', 'SPEED Four', 'SPEED TRIPLE', 'SPEED TRIPLE ABS', 'SPEED TRIPLE RS', 'SPEED Triple R', 'STREET TRIPLE', 'STREET TRIPLE 660', 'STREET TRIPLE R', 'STREET TRIPLE RS', 'STREET TRIPLE S', 'STREET TRIPLE S 660', 'Speed Triple S', 'Speedmaster 800', 'Speedmaster 900', 'Street Triple R', 'Street Triple R x', 'Street Twin', 'TIGER 1050', 'TIGER 800', 'TIGER 800 XC', 'TIGER 800 XC X', 'TIGER Explorer 1200', 'TIGER Explorer 1200 XC', 'TIGER Explorer 1200 XCA', 'TIGER Explorer 1200 XR', 'Thruxton EFI', 'ThruxtonRS', 'Tiger 800 XR X'), 'APRILIA': ('Caponord', 'Dorsoduro 750', 'RS 660', 'RSV 4 R APRC', 'RSV Mille Tuono', 'RSV4 RR', 'SMV 750 Dorsoduro', 'SMV 750 Dorsoduro ABS', 'SRV 850', 'SX 125', 'Shiver 750', 'Shiver 750 GT', 'Shiver 900', 'Sportcity 125', 'Tuono 1000 R', 'Tuono 125', 'Tuono V4 1100 Factory'), 'KAWASAKI': ('ER 5', 'ER 6F', 'ER 6N', 'GTR 1400', 'J 125', 'Ninja 1000 SX', 'Ninja H2 SX SE', 'Ninja H2 SX SE +', 'VERSYS 1000', 'VERSYS 650', 'VN 1600 CLASIC', 'VN VULCAN 800 CLASIC', 'Versys 650 ABS', 'Vulcan S', 'Z 1000', 'Z 1000 SX', 'Z 750', 'Z 800e', 'Z 900', 'ZX 10R', 'ZX 10R KRT', 'ZX 6R', 'ZX 6R 636', 'ZX-10RR', 'ZX6R', 'ZZR 1400'), 'PEUGEOT': ('Citystar 125 ABS', 'Django 50 Allure', 'Django50Heritage', 'Metropolis 400', 'Metropolis 400 RX-R', 'SATELIS 125i urban'), 'HONDA': ('CB 1000R', 'CB 500 F', 'CB 500 X', 'CB 500 X ABS', 'CB 500F', 'CBF 1000', 'CBF 500', 'CBF 600N', 'CBF 600S', 'CBR 1000 RR Fireblade', 'CBR 1000RR', 'CBR 1000RR Fireblade', 'CBR 1100 XX', 'CBR 600 RR', 'CBR 600F', 'CBR 650 F', 'CBR 650F', 'CRF 250 RX', 'CRF 450 L', 'CRF1000L Africa Twin', 'CRF1000L Africa Twin DCT', 'CTX 700', 'Crossrunner VFR800X', 'FMX 650', 'FORZA 250 EX', 'FORZA 250 X', 'Forza 125', 'Forza 300', 'Integra', 'NC 700 S', 'NC 750 S', 'NC 750 S DTC ABS', 'NC 750 X DCT', 'NT 650 V DEAUVILLE', 'NT 700 DEAUVILLE', 'NT 700 V DEAUVILLE', 'NTV 650 REVERE', 'PAN-EUROPEAN ST 1300', 'Passion 125 I.E.', 'Rebel 500', 'S-WING 125', 'SCOOPY SH300i', 'SCOOPY SH300i TopBox', 'SILVER WING 600', 'TRANSALP XL 650 V', 'VARADERO XL1000V', 'VFR 1200 F', 'VFR 1200 F DCT', 'VFR 800 FI', 'VT 750 C SHADOW', 'X-ADV', 'XL 125V'), 'SYM': ('CruisymAlpha300', 'Fiddle 125', 'Fiddle III', 'HD 300', 'JOYMAX 125', 'JOYMAX 300i ABS S&S Sport', 'Jet 4 50 4T', 'MAXSYM 400', 'MAXSYM 600i ABS Sport', 'Maxsym 600i ABS', 'Mio 115', 'Symphony ST 200i CBS'), 'YAMAHA': ('FJR 1300 A', 'FJR 1300 AE', 'FZ1 N', 'FZ6 N', 'FZ6 S', 'FZ6 S ABS', 'FZ8 N', 'MT 01', 'MT 03', 'MT 09', 'MT10', 'MT10 SP', 'Majesty 400', 'Niken', 'Super Ténéré', 'T-Max 500', 'T-Max 500 ABS', 'TMAX 560 TECH MAX', 'V-Max 1200', 'V-Max 1700', 'X MAX 125 Iron Max', 'X MAX 250', 'X MAX 400', 'X MAX 400 ABS', 'X enter 125', 'X-CITY 250', 'X-MAX 125', 'X-MAX 250 Momodesing', 'X-MAX 300', 'X-MAX 400', 'XJ6 Diversion N', 'XJR 1300', 'XSR900 ABS', 'XT 660 X', 'XV 1100 Virago', 'XVS 650 A Drag Star Classic', 'XVS 650 Drag Star Classic', 'XVZ 1300 Royal Star Venture', 'YP Majesty 150', 'YZF R 125', 'YZF R1', 'YZF R6', 'YZF R6R', 'YZF-R3'), 'HUSQVARNA': ('701 Supermoto', 'SVARTPILEN 401', 'Svartpilen 701', 'Vitpilen 701'), 'MOTO GUZZI': ('V7 II Racer', 'V7 III Stone', 'V9 Roamer'), 'ROYAL ENFIELD': ('Meteor 350',), 'DUCATI': ('1098 SUPERBIKE', '1299 Panigale S Anniversario', '749 R', '848 Superbike', 'DIAVEL 1198', 'DIAVEL Dark', 'Diavel', 'HYPERMOTARD 1000', 'Hypermotard 939', 'Hyperstrada', 'MONSTER 1100', 'MONSTER 1200', 'MONSTER 620', 'MONSTER 696', 'MONSTER 796', 'MONSTER S2R 1000', 'MONSTER S2R 800', 'MONSTER796', 'MULTISTRADA 1000 DS', 'MULTISTRADA 1100', 'MULTISTRADA 1200', 'MULTISTRADA 1200 S Sport', 'MULTISTRADA 620', 'Multistrada 1260 S', 'Scrambler 1100', 'Scrambler Café Racer', 'Scrambler Classic', 'Scrambler Desert Sled', 'Scrambler Sixty2', 'Streetfighter 1100', 'Streetfighter V4', 'SuperSport'), 'KTM': ('1050 Adventure', '1090 Adventure R', '1190 Adventure', '125 Duke', '1290 Super Adventure', '1290 Super Adventure R', '1290 Super Adventure T', '1290 Super Duke GT', '1290 Super Duke R ABS', '250 EXC-F', '300 EXC', '390 Duke', '690 DUKE', '690 SMC R ABS', '790 Duke', '890 Adventure', '950 Adventure', '990 SUPER DUKE', 'DUKE II', 'EXC 300', 'Freeride 250 F', 'LC4 620 SUPERCOMPETICION', 'RC8 1150'), 'BMW': ('C 400 X', 'C 600 Sport', 'C 650 GT', 'C 650 Sport', 'F 650', 'F 650 GS', 'F 700 GS', 'F 800 GS', 'F 800 GS Adventure', 'F 800 GT', 'F 800 R', 'F 800 R 2015', 'F 800 S', 'F 800 ST', 'F 900 XR', 'G 310 GS', 'G 310 R', 'G 650 GS', 'K 1200 GT', 'K 1200 LT', 'K 1200 R', 'K 1200 R Sport', 'K 1200 RS', 'K 1200 S', 'K 1300 GT', 'K 1300 R', 'K 1300 S', 'K 1600 GT', 'K1200R', 'R 1200 GS', 'R 1200 GS 105cv', 'R 1200 GS 98cv', 'R 1200 GS Adventure', 'R 1200 GS Adventure 105cv', 'R 1200 R', 'R 1200 RT', 'R 1200 RT 110cv', 'R 1200 S', 'R 1250 R', 'R 1250 RT', 'R 850 R', 'R nineT', 'R nineT Racer', 'R nineT Scrambler', 'R nineT Urban GS', 'S 1000 R', 'S 1000 RR', 'S 1000 XR'), 'SUZUKI': ('B-KING 1340', 'BURGMAN 125', 'BURGMAN 200', 'BURGMAN 400', 'BURGMAN 650 Executive', 'Bandit 650 S', 'GS 500', 'GSF 600 Bandit S', 'GSR 600', 'GSR 750', 'GSR750', 'GSX 1250 FA', 'GSX 650 F', 'GSX R1000', 'GSX R600', 'GSX R750', 'GSX-R1000R', 'GSX-S 1000', 'GSX-S 1000 F', 'GSX-S125 ABS', 'GSX250R/ABS', 'Gladius 650', 'Gladius 650 ABS', 'Hayabusa 1300', 'Intruder C1500', 'Intruder C800', 'LS 650 Savage', 'Marauder 250', 'V-Strom 1000', 'V-Strom 1000 ABS', 'V-Strom 650', 'V-Strom 650 ABS', 'VL 800 Intruder Volusia', 'VanVan 125'), 'KYMCO': ('AK 550', 'Agility CITY 125', 'Grand Dink 125', 'Like 125', 'People 50 S', 'Super Dink 125 ABS', 'Super Dink 350i', 'Xciting 400i'), 'HARLEY DAVIDSON': ('Dyna Low Rider', 'Dyna Switchback', 'Softail Slim', 'Sportster 1200', 'Sportster 1200 Custom', 'Sportster 883', 'Sportster 883 Iron', 'Sportster 883 Superlow', 'Sportster Forty-Eight', 'Sportster Superlow 1200T', 'Sportster XR 1200', 'Street 750', 'Touring Electra Glide Classic', 'VRSC Night Rod Special', 'VRSC V-Rod', 'VRSC V-Rod Muscle', 'VRSCA V-Rod Screaming Eagle'), 'MV AGUSTA': ('BRUTALE 1090 RR', 'BRUTALE 750S', 'BRUTALE 800', 'BRUTALE 800 EAS ABS', 'BRUTALE 800 RR', 'BRUTALE 990 R', 'Dragster 800 RR America', 'Turismo Veloce 800 Lusso'), 'GAS GAS': ('EC 250 R', 'EC 350 F'), 'VESPA': ('Elettrica L1', 'GTS 300 Super', 'LXV 50 2T', 'Primavera 125', 'Primavera 50 2T', 'S 125 ie'), 'PIAGGIO': ('Beverly 350 ABS', 'Beverly 400 HPE', 'LIBERTY 50 I-GET', 'MP3 350 ABS/ASR', 'MP3 500 Sport ABS/ASR', 'X EVO 400', 'X10 350 ie', 'beverly 300 ie', 'beverly Sport Touring 350 ie'), 'HUSABERG': ('TE 250',), 'ZONTES': ('X-310',), 'BENELLI': ('502 C', 'BN 251', 'BN 251 ABS', 'Leoncino 250', 'TRK 251', 'TRK 502'), 'FANTIC': ('Caballero Flat Track 500',), 'MASH': ('Cafe Racer', 'Five Hundred', 'Seventy Five', 'X-Ride 650'), 'HANWAY': ('Raw 125 Cafe', 'Scrambler 125'), 'DAELIM': ('XQ2 300',), 'MACBOR': ('Lord Martin 125', 'Montana XR3', 'Shifter MC1'), 'LML': ('STAR 200 4T Deluxe',), 'CFMOTO': ('650 MT',), 'GOES': ('G 125 GT',), 'GILERA': ('Nexus 300',), 'SWM': ('Super Dual T',), 'MOTOR HISPANIA': ('REVENGE',), 'ORCAL': ('Astor 125',), 'MITT': ('125 PK',), 'FKM': ('Street Scrambler 125',), 'DERBI': ('Variant Sport 50',), 'INDIAN': ('FTR 1200',), 'QUADRO': ('QV3',), 'RIEJU': ('Century',)}
brands = ('APRILIA', 'BENELLI', 'BMW', 'CFMOTO', 'DAELIM', 'DERBI', 'DUCATI', 'FANTIC', 'FKM', 'GAS GAS', 'GILERA', 'GOES', 'HANWAY', 'HARLEY DAVIDSON', 'HONDA', 'HUSABERG', 'HUSQVARNA', 'INDIAN', 'KAWASAKI', 'KTM', 'KYMCO', 'LML', 'MACBOR', 'MASH', 'MITT', 'MOTO GUZZI', 'MOTOR HISPANIA', 'MV AGUSTA', 'ORCAL', 'PEUGEOT', 'PIAGGIO', 'QUADRO', 'RIEJU', 'ROYAL ENFIELD', 'SUZUKI', 'SWM', 'SYM', 'TRIUMPH', 'VESPA', 'YAMAHA', 'ZONTES')

# embed streamlit docs in a streamlit app
#components.iframe("https://docs.streamlit.io/en/latest")
st.set_page_config(
     page_title="Mundimoto",
     page_icon="🏍️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
st.title('Mundimoto🏍️')
st.header('Calcula el valor de tu motocicleta')
st.subheader('Sin compromisos, sin mentiras')
#[theme]
#primaryColor="#000000"
#backgroundColor="#000000"
#secondaryBackgroundColor="#000000"
#textColor="#262730"
#font="sans serif"
brand = st.selectbox("Marca", brands)
terminos=False
name = st.selectbox("Modelo", models.get(brand))
kms = st.slider(
     'Seleccione los kilometros que tiene su motocicleta',0,1000000,100)#falta especificar valores realistas
license = st.radio("Seleccione la licencia o licencias que permiten conducir su motocicleta", ['A','A1','A2','AB'])
cilindrada = st.radio("Seleccione la cilindrada der su motocicleta", ['49','125','250','500','700','1000','1500','2000'])

year = st.slider("Año de matriculación", 1985,2022,2008)
cycleType = st.selectbox('Seleccione el tipo de moto que más se ajusta',('SCOOTER','MAXI-SCOOTER','CLASSIC','NAKED','SPORT','TOURING','TRAIL','OFF-ROAD','CUSTOM','TRES RUEDAS'))
typeImage = Image.open('images/'+cycleType+'Type.png')
st.image(typeImage)
color = st.color_picker('Seleccione el color de su motocicleta', '#00f900')
if st.checkbox('Acepto los términos y condiciones'):
	terminos = True
if st.button('Dame un super precio!!'):
	if terminos:
		if not name:
			st.warning('Porfavor complete el modelo de su motocicleta')
			st.stop()
		#with st.spinner('Calculando precio aproximado...'):
    #			time.sleep(5)
		st.success('Precio calculado satisfactoriamente :sunglasses:')
		st.balloons()
		data_set = {"brand":brand, "name":name, "kms":kms, "license":license, "year":year, "cycleType":cycleType, "capacity":cilindrada}
		json_dump=json.dumps(data_set)
		r = requests.post(url='http://127.0.0.1:8000/api/predictor/', data=data_set)
		st.success('El precio por el que tasaríamos su moto es de: ' + r.text +' € :sunglasses:')
		#enviar data a mi amigo del departamento del back-end
	else:
		st.warning('Porfavor, acepte los terminos y condiciones para continuar ')
