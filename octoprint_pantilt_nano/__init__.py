# coding=utf-8
from __future__ import absolute_import

import serial

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin


class Pantilt_nanoPlugin(octoprint.plugin.SettingsPlugin,
						 octoprint.plugin.AssetPlugin,
						 octoprint.plugin.TemplatePlugin,
						 octoprint.plugin.StartupPlugin,
						 octoprint.plugin.ShutdownPlugin):
	def __init__(self):
		self.serial = None

	##~~ SettingsPlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			port='/dev/ttyUSB0',
			baud=9600,
			pan=dict(
				minUs=1000,
				maxUs=2000,
				invert=False
			),
			tilt=dict(
				minUs=1000,
				maxUs=2000,
				invert=False
			)
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/pantilt_nano.js"],
			css=["css/pantilt_nano.css"],
			less=["less/pantilt_nano.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			pantilt_nano=dict(
				displayName="PanTilt_Nano Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="you",
				repo="OctoPrint-PanTilt_Nano",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/you/OctoPrint-PantTilt_Nano/archive/{target_version}.zip"
			)
		)

	##~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info('opening serial port {}'.format(self._settings.get(['port'])))
		self.serial = serial.Serial()
		self.serial.baudrate = self._settings.get(['baud'])
		self.serial.port = self._settings.get(['port'])
		try:
			self.serial.open()
			self.serial.setDTR(True)
		except Exception as e:
			self._logger.info('Error opening {} : {}'.format(self._settings.get(['port']), e))

	##~~ ShutdownPlugin
	def on_shutdown(self):
		self._logger.info("Closing serial port {}".format(self._settings.get(['port'])))
		self.serial.close()

	##~~ pantilt_handler handler
	def handle_pantilt(self, pan, tilt):
		panVal = int(pan) / 100.0 * (self._settings.get(["pan", "maxUs"]) - self._settings.get(["pan", "minUs"])) + self._settings.get(["pan", "minUs"])
		tiltVal = int(tilt) / 100.0 * (self._settings.get(["tilt", "maxUs"]) - self._settings.get(["tilt", "minUs"])) + self._settings.get(["tilt", "minUs"])
		self._logger.info('{{command:set, target:panUs, value:{}}}\n'.format(int(panVal)))
		self._logger.info('{{command:set, target:tiltUs, value:{}}}\n'.format(int(tiltVal)))
		if self.serial is not None and self.serial.isOpen():
			self.serial.write('{{command:set, target:panUs, value:{}}}\n'.format(int(panVal)).encode())
			self.serial.flush()
			self._logger.info(self.serial.readline())
			self.serial.write('{{command:set, target:tiltUs, value:{}}}\n'.format(int(tiltVal)).encode())
			self.serial.flush()
			self._logger.info(self.serial.readline())


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Pantilt_nano Plugin"


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Pantilt_nanoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.plugin.pantilt_handler": __plugin_implementation__.handle_pantilt
	}
