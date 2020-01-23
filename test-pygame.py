import pygame
import sys, time, subprocess
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

filename = "recording.wav"
imageFilename = "spectrogram.png"
white = (255,255,255)

def initPygame():
	pygame.init()
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	return screen

def importAudio():
	p1 = subprocess.Popen(["rtl_fm","-f","98.4e6","-s","44100","-"],stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["sox","-t","raw","-e","signed-integer","-c","2","-b","16","-r","44100","-",filename],stdin=p1.stdout)
	p1.stdout.close()
	try:
		outs, errs = p2.communicate(timeout=1.5)
	except subprocess.TimeoutExpired:
		p2.terminate()
		outs, errs = p2.communicate()
	time.sleep(0.5)

def processWaveFile():
	# start processing of wav file
	print("begin to draw")
	# draw spectrogram
	rate, audio = wavfile.read(filename)
	#convert to mono
	audio = np.mean(audio, axis=1)

	#Then, we calculate the length of the snippet and plot the audio
	N = audio.shape[0]
	L = N / rate
	M = 1024
	print(f'Audio length: {L:.2f} seconds')

	freqs, times, Sx = signal.spectrogram(audio, fs=rate, window='hanning',
	                                      nperseg=1024, noverlap=M - 100,
	                                      detrend=False, scaling='spectrum')
	fig = plt.figure(figsize=(3,2))
	#fig.add_axes([0,0,1,1])
	ax = fig.add_subplot(111)
	ax.axis("off")
	ax.pcolormesh(times, freqs / 1000, 10 * np.log10(Sx), cmap='viridis')
	plt.savefig(imageFilename)
	# ending
	print("done.")

def main():	
	# init PyGame
	screen = initPygame()

	# main loop
	while (True):
		# check for quit events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		# run rtl_fm and save data as wav
		importAudio()

		# process wav file
		processWaveFile()

		plt.close('all')
		img = pygame.image.load(imageFilename)

		# erase the screen
		screen.fill(white)

		# draw the updated picture
		screen.blit(img, (0,0))

		#updatePoints(points)  # changes the location of the points
#		pygame.draw.lines(screen, black, False, [(100,100), (150,200), (200,100)], 1)

		# update the screen
		pygame.display.update()

if __name__ == '__main__':
	main()

