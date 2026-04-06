from enigma import eDVBVolumecontrol  # this is not nice
from Components.Sources.Source import Source
from GlobalActions import globalActionMap


class Volume(Source):
	def __init__(self, session):
		Source.__init__(self)
		global globalActionMap  # hackalert :)
		self.actionmap = globalActionMap
		self.volctrl = eDVBVolumecontrol.getInstance()  # this is not nice
		self.vol = (True, "State", self.volctrl.getVolume(), self.volctrl.isMuted())

	def handleCommand(self, cmd):
		lst = []
		if cmd == "state":
			lst.extend((True, _("State")))
		elif cmd == "up":
			self.actionmap.actions["volumeUp"]()
			lst.extend((True, _("Volume changed")))
		elif cmd == "down":
			self.actionmap.actions["volumeDown"]()
			lst.extend((True, _("Volume changed")))
		elif cmd == "mute":
			self.actionmap.actions["volumeMute"]()
			lst.extend((True, _("Mute toggled")))
		elif cmd.startswith("set"):
			try:
				targetvol = int(cmd[3:])
				if targetvol > 100:
					targetvol = 100
				if targetvol < 0:
					targetvol = 0

				self.volctrl.setVolume(targetvol, targetvol)

				lst.extend((True, _("Volume set to %i") % targetvol))
			except ValueError:  # if cmd was set12NotInt
				lst.extend((False, _("Wrong parameter format 'set=%s'. Use set=set15") % cmd))
		else:
			lst.extend((False, _("Unknown Volume command %s") % cmd))

		lst.extend((self.volctrl.getVolume(), self.volctrl.isMuted()))

		self.vol = lst

	volume = property(lambda self: self.vol)
