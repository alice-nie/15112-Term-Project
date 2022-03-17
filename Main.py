# master file -- run this for the game

from cmu_112_graphics import *
from Calendar import *
from Room import *
from OmniBox import *
from StatBars import *
from DatingSim import *
from Quest import *

# import lines from https://www.cs.cmu.edu/~112/notes/term-project.html
import module_manager
module_manager.review()
# encountered an error with user permission and troubleshooted using 
# https://superuser.com/questions/1482757/homebrew-error-message-osx and https://people.csail.mit.edu/hubert/pyaudio/


# got import lines and learned about pygame mixer at https://www.youtube.com/watch?v=pcdB2s2y4Qc&feature=emb_logo&ab_channel=buildwithpython 
# and https://www.pygame.org/docs/ref/mixer.html
import pygame
from pygame import mixer
# music is taken from game: Doki Doki Literature Club by Team Salvatore
# Downloaded from https://www.youtube.com/watch?v=BFSWlDpA6C4&list=PLc5ZKngbAPXMG4yjq9ESGfqblQfL9g4-p&index=1&ab_channel=TeamSalvato
# using https://ytmp3.cc/en13/ and https://cloudconvert.com/mp3-to-wav for audio conversion


# following CMU 112 graphics framework
# following "Subclassing ModalApp and Mode" code and format from https://www.cs.cmu.edu/~112/schedule.html
# Any images are drawn by Nhu Tat. Her email: ntat@andrew.cmu.edu

class MyModalApp(ModalApp):

	def appStarted(self):
		# from https://www.pygame.org/docs/ref/mixer.html
		pygame.mixer.init()
		
		self.room = Room()
		self.calendar = Calendar()
		self.omniBox = OmniBox()
		self.statBars = StatBars()
		self.datingSim = DatingSim()
		self.quest = Quest()
		self.setActiveMode(self.room) 
		
		if self._activeMode == self.room:
			# code from https://www.youtube.com/watch?v=pcdB2s2y4Qc&feature=emb_logo&ab_channel=buildwithpython
			mixer.music.load('DDLC main.wav')
			mixer.music.play(-1)

	

app = MyModalApp(width=1440, height = 778)

# from https://www.pygame.org/docs/ref/mixer.html
mixer.music.stop()
