from sys import exit
import random
from random import randint
from content import *
from engine import *
from questions import *


class Scene(object):

	# initialises each instance of Scene
	def __init__(self):
		self.name = None
		self.description = None
		self.visit = 0

	def enter(self):
		exit(1)

	def user_input(self):
		choice = raw_input(prompt)
		lowercase = choice.lower()
		key_words = lowercase.split(' ')
		return key_words


class Death(Scene):

	scoffs = [
		"Sorry! Try again soon :)",
		"Oh no! Better luck next time :)",
		"Nevermind! Tomorrow is another day :)"
	]

	def enter(self):
		print Death.scoffs[randint(0, len(self.scoffs)-1)]
		exit(1)


# Pre-game greeting scene where the players name is established.

class Greeting(Scene):

	def enter(self):
		name = raw_input("What's your name? ")
		split = name.split(' ')
		first = split.pop(0)
		print "May I call you %s?" % first

		confirm = raw_input(prompt)
		global title
		if confirm.lower() in affirm:
			title = first
			print "Great. Good to meet you %s" % first
		elif confirm.lower() in negate:
			title = raw_input("What shall we call you then? ")
			print "Cool. Lovely to meet you %s" % title
		else:
			print "Sorry, I don't understand. Let's just call you Buddy"
			title = 'Buddy'


	def action(self):
		return 'wake_room'
		

# First scene - player wakes in a strange room and has to choose between a tunnel or shaft.

class WakeRoom(Scene):

	def enter(self):
		if self.visit == 0:	
			print wake_room_intro
			self.visit += 1
		else:
			print "What'll it be, tunnel or ventilation shaft?"

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i in theWheelRoom:
				return 'wheel_room'
			elif i in pixieRoom:
				return 'pixie'
		print nonono + title + "."
		return 'wake_room'


# Room with spinning wheel and 3 further doors.

class WheelRoom(Scene):

	def enter(self):
		print """
		OK %s, you head through the tunnel, gagging at the rancid smell and
		desperately trying to avoid the rusty, jagged metal protruding from the
		walls. You reach a grate at the far end. It takes multiple kicks to
		break it down, but finally it flies off and you climb down into a large
		room.\n
		In it you find three doors and a spinning wheel divided into thirds.
		Next to it, a message reads:
		""" % title

		print message

	def action(self):

		key_words = Scene.user_input(self)

		for i in key_words:
			if i in affirm or i in spin:
				number = random.randint(0,7)

				print spin_text

				if int(number) in range(0,3):
					return 'child'
				elif int(number) in range(3,6):
					return 'space_time'
				else:
					print wrong_way
					return 'wake_room'

			elif i in negate:
				return 'death'
		print nonono + title + "."
		return WheelRoom.action(self)

# Room with child who holds a bottle and a key for you to choose between.

class Child(Scene):

	def enter(self):
		print child_room_intro
		print "Hello %s, I hope you've had a pleasant journey so far. In one hand I hold the key to your salvation, in the other, your doom. I wish I could tell you which was which, but only you can decide your fate." % title

	def action(self):
		key_words = Scene.user_input(self)

		for i in key_words:
			if i in child_bottle:
				print bottle_text
				return Child.either_door(self)
			elif i.lower() in child_key:
				print key_text
				return 'death'
		print nonono + title + "."
		return Child.action(self)

	def either_door(self):
		key_words = Scene.user_input(self)

		for i in key_words:
			if i == 'east':
				print "Looks like we're off to see the Wizard, %s!" % title
				return 'wizard'
			elif i == 'west':
				print "Let's hope there's still some fight left in you, %s" % title
				return 'ninja'
			
		print nonono + title + "."
		return Child.either_door(self)


# Room with teleportation device and time machine.

class SpaceTime(Scene):

	def enter(self):
		print space_time_intro

	def action(self):
		key_words = Scene.user_input(self)

		for i in key_words:
			if i in time_machine:
				return 'historian'
			elif i in teleportation:
				print "Dammit. The stupid thing teleports you back to the start!"
				return 'wake_room'
		print nonono + title + "."
		return SpaceTime.action(self)

# Walled garden with sleeping pixie.

class Pixie(Scene):

	def enter(self):
		if self.visit == 0:
			print pixie_intro
			self.visit = 1
		else:
			print pixie_intro_mini
		# pixy_woken = False

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i in pixieCross1:
				print "Woah, big mistake %s. Never touch a sleeping pixie. For that matter, never approach any sleeping stranger and start touching them. That's just bad manners." % title
				return 'death'
			elif i in pixieHappy1:
				print "She wakes up. Do you make polite chitchat or just get straight down to business?"
				
				key_words = Scene.user_input(self)
				for i in key_words:
					if i in pixieCross2:
						print "Nooo! Haven't you ever heard the saying, \"Never make small-talk with a pixy? They HATE it.\""
						return 'death'
					elif i in pixieHappy2:
						print "Good. Pixies appreciate brevity. She unlocks the door for you."
						return 'empty_room'	

				print "What? Bored with your nonesense, she falls back to sleep."
				print "Let's try this again...whisper in her ear or tap her on the shoulder?"
				return Pixie.action(self)

		print nonono + title + "."
		return Pixie.action(self)


# Wizard/Sorcerer who presents you with a riddle

class Wizard(Scene):

	def enter(self):
		print wizard_intro

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i in affirm:
				print "A wise decision %s" % title
				return 'riddle'
			elif i in negate:
				print "Furious at your insubordination, she turns you into a coffee table anyway"
				return 'death'
		print nonono + title + "."
		return Wizard.action(self)


# Riddle of the 3 people and 5 hats.

class Riddle(Scene):

	def enter(self):
		print riddle_text

	def action(self):
		choice = raw_input(prompt)
		lowercase = choice.lower()

		if "purple" and "red" in lowercase:
			print "That's cheating. You get one guess"
			return Riddle.action(self)
		elif "purple" in lowercase:
			print "Yay! The sorcerer applauds you on your riddle mastery and sends you on your way."
			return 'over'
		elif "red" in lowercase:
			print "Nooooo!"
			return 'death'
		else:
			return 'death'


# First Ninja scene, fight setup.

class Ninja(Scene):

	def enter(self):
		print ninja_intro

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i in affirm:
				strategy = raw_input("roundhouse to the face or jumping sidekick to the groin? ")
				lower = strategy.lower()
				key_words = lower.split(' ')
				for i in key_words:

					if i in ninja_kick1:
						return 'smash'
					elif i in ninja_kick2:
						return 'brutal'					
				print "I'm afraid I don't know what a %s is " % strategy + title + "." + "Are you sure you want to fight?"
				return Ninja.action(self)

			elif i in negate:
				print "Lucky for you, this ninja has a soft spot for pacifists.\n You win, simply in virtue of being a decent human being"
				return 'over'
			
		print nonsense + title + "."
		return Ninja.action(self)

# First section of ninja fight

class Smash(Scene):

	def enter(self):
		print "Nice shot! He's stunned, how're you going to finish him: elbow or backfist?"

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i == "elbow":
				print "BOOM! He's down. There's no denying it, you're a badass!"
				return 'over'
			elif i == "backfist":
				print "He ducks. Come on, you can do this. One more strike and he's down.\n Have you got one more left in you?"
				finish_him = raw_input(prompt)
				lower = finish_him.lower()
				split = lower.split(' ')
				for i in split:
					if i in affirm:
						luck = random.randint(0,2)

						if luck <= 1:
							print "You did it! He begs you for mercy. You walk away, head held high."
							return 'over'
						else:
							print "Noooo! He's just too quick for you."
							return 'death'

					elif i in negate:
						print "He floors you. Oh dear!"
						return 'death'
					
				print nonono + title + "."
				return action.luck

		print nonono + title + "."
		return Smash.action

# Additional section of Ninja fight.

class Brutal(Scene):

	def enter(self):
		print "\nOuch! He goes flying, but comes back pissed off. Before you know it he's leaping through the air, his foot rapidly approaching your face. Do you jump left, right, or duck?"

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i == "left":
				left = random.randint(0,2)

				if left == 0:
					print ninja_miss_side
					return 'over'
				else:
					print ninja_hit
					return 'death'

			elif i == "right":
				right = random.randint(0,2)

				if right == 0:
					print ninja_miss_side
					return 'over'
				else:
					print ninja_hit
					return 'death'

			elif i == "duck":
				duck = random.randint(0,2)

				if duck == 0:
					print ninja_miss_duck
					return 'over'
				else:
					print ninja_hit
					return 'death'
		
		print nonono + title + "."
		return action

class EmptyRoom(Scene):

	def enter(self):
		if self.visit == 0:
			print empty_room_intro
		else:
			print "OK, let's try this again." + empty_room_intro
		self.visit =+ 1

	def action(self):
		choice = raw_input(prompt)
		# try:
		# 	return int(choice)
		if "1" in choice:
			print "Uh oh, back we go."
			return 'wake_room'
		elif "2" in choice:
			print "Coolios"
			return 'ocean'
		elif "3" in choice:
			print "Awesome."
			return 'godot'
		else:
			print "1, 2 or 3. Was that really too much to ask for?"
			return EmptyRoom.action(self)
		# except valueError:
		# 	print "Just a number, please."
		# 	return EmptyRoom.action


class Ocean(Scene):

	def enter(self):
		print ocean_intro

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					return 'tortoise'
				elif which_q == 1:
					return 'overshoot'
				else:
					return 'greenpeace'

			elif i in negate:
				print defeatism
				return 'death'
			
		print nonono + title + "."
		return Ocean.action(self)

class Tortoise(Scene):

	def enter(self):
		print tortoise_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i == "2012":
				print wrong_ocean_a
				return 'death'
			elif i == "2013":
				print wrong_ocean_a
				return 'death'
			elif i == "2014":
				print right_ocean_a
				return 'over'
			
		print nonono + title + "."
		return Tortoise.action

class Overshoot(Scene):

	def enter(self):
		print overshoot_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i == "August":
				print right_ocean_a
				return 'over'
			elif i == "September":
				print wrong_ocean_a
				return 'death'
			elif i == "October":
				print wrong_ocean_a
				return 'over'
			
		print nonono + title + "."
		return Overshoot.action

class Greenpeace(Scene):

	def enter(self):
		print greenpeace_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i in greenpeace_a:
				print right_ocean_a
				return 'over'
			else:
				print wrong_ocean_a
				return 'death'



class Historian(Scene):

	def enter(self):
		print historian_intro

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					return 'war'
				elif which_q == 1:
					return 'acidification'
				else:
					return 'poverty'

			elif i in negate:
				print defeatism
				return 'death'
		
		print nonono + title + "."
		return Historian


class War(Scene):

	def enter(self):
		print war_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i == "15th":
				print wrong_history_a
				return 'death'
			elif i == "17th":
				print wrong_history_a
				return 'death'
			elif i == "19th":
				print "Congratulations, our historian is super impressed with your knowledge. She takes you on a tour of 2523, and even let's you take a souvenir home with you."
				return 'over'
		print nonono + title + "."
		return War.action(self)

class Acidification(Scene):

	def enter(self):
		print acidification_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:

			if i == "200":
				print wrong_history_a
				return 'death'
			elif i == "300":
				print "Correct. Scientists estimate that, as a consequence, sea oxygen levels will have dropped by as much as 7% by 2100."
				return 'over'
			elif i == "400":
				print wrong_history_a
				return 'death'
			
		print nonono + title + "."
		return Acidification.action

class Poverty(Scene):

	def enter(self):
		print poverty_q

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i == "1.50":
				print wrong_history_a
				return 'death'
			elif i == "1.90":
				print "That's right. $1.90. A day. Did I mention, in 2012, 896 million people were still living below this line?"
				return 'over'
			elif i == "2.25":
				print wrong_history_a
				return 'death'

		print nonono + title + "."
		return Poverty.action


class Godot(Scene):

	def enter(self):
		print godot_intro

	def action(self):
		key_words = Scene.user_input(self)
		for i in key_words:
			if i in affirm:
				print godot_outro
				return 'over'
			elif i in negate:
				print "And so your life continues in much the same fashion as before this strange episode."
				return 'over'
		print "They all disappear in a puff of smoke."
		return 'over'

class Over(Scene):

	def enter(self):
		print "Play again, or go do something productive with your day?"
		key_words = Scene.user_input(self)
		for i in key_words:
			if i in play_again:
				print wake_room_intro
				a_map = Map("wake_room")
				a_game = Engine(a_map)
				a_game.play()
			elif i in do_something:
				print "Good for you! Go be in nature, fall in love, create something, experience some life. "
				exit(1)


class Map(object):   # Creates a map of the game with a dictionary of Scene instances.
	scenes = {
	'death': Death(),
	'greeting': Greeting(),
	'wake_room': WakeRoom(),
	'wheel_room': WheelRoom(),
	'pixie': Pixie(),
	'empty_room': EmptyRoom(),
	'wizard': Wizard(),
	'riddle': Riddle(),
	'child': Child(),
	'space_time': SpaceTime(),
	'historian': Historian(),
	'war': War(),
	'acidification': Acidification(),
	'poverty': Poverty(),
	'over': Over(),
	'ocean': Ocean(),
	'tortoise': Tortoise(),
	'overshoot': Overshoot(),
	'greenpeace': Greenpeace(),
	'godot': Godot(),
	'ninja': Ninja(),
	'smash': Smash(),
	'brutal': Brutal(),
	}

	def __init__(self, start_scene_key):
		self.start_scene_key = start_scene_key

	def next_scene(self, scene_name):
		val = Map.scenes.get(scene_name)
		return val

	def opening_scene(self):
		return self.next_scene(self.start_scene_key)


a_map = Map('greeting')   # sets a_map to an instance of class Map, with parameter 'greeting'.
a_game = Engine(a_map)   # sets a_game to an instance of class Engine, with the parameter 'a_map'
a_game.play()    # from Engine instance a_game, calls the play() method.