import png

#Note
#For high contrast images, a detail level of 1 is recommended
#Anything above 2 is usually clearly visible

#Usage
#Run create() to hide msg.png in org.png's least significant bits
#Run reverse() to get the hidden picture out of res.png

def create(detail = 2):
	with open("org.png", "rb") as ifsorg, open("msg.png", "rb") as ifsmsg:
		org = png.Reader(file=ifsorg)
		msg = png.Reader(file=ifsmsg)

		orgar = org.read()
		msgar = msg.read()
		if orgar[0] < msgar[0] or orgar[1] < msgar[1]:
			print("Wrong sizes")
			exit()
	
		
		h = msgar[1]
		w = msgar[0]
		
		gsmsg = orgar[3]["planes"] // msgar[3]["planes"]  #this is usually 1, unless msg is grayscale
		if gsmsg == 0:
			print("Message contains more channels than origin")
			exit()
		
		orgar = list(orgar[2])
		msgar = list(msgar[2])
		
		
		
		
		for y in range(h):
			for x in range(w):
				for i in range(3*x, 3*x+3):
					msgbit = int(msgar[y][i//gsmsg])
					orgar[y][i] = (orgar[y][i]>>detail<<detail) + (msgbit>>(8-detail))

		
		
		
		
		with open("res.png", "wb") as ofs:
			writer = png.Writer(w,h, greyscale = False)
			writer.write(ofs, orgar)

def reverse(detail = 2):

	with open("res.png", "rb") as ifsres:
		res = png.Reader(file=ifsres)
		resar = res.read()
		
		h = resar[1]
		w = resar[0]
		
		resar = list(resar[2])
		for y in range(h):
			for x in range(w):
				for i in range(3*x, 3*x+3):
					resar[y][i] = (resar[y][i]<<(8-detail))%256
					resar[y][i] += (1<<(7-detail)) #average out data loss
		
		with open("bac.png", "wb") as ofs:
			writer = png.Writer(w,h, greyscale = False)
			writer.write(ofs, resar)