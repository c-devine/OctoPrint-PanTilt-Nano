# coding=utf-8
from __future__ import absolute_import
from __future__ import division
import serial
import octoprint.plugin
import octoprint.util.comm as comm


class Pantilt_nanoPlugin(octoprint.plugin.SettingsPlugin,
						 octoprint.plugin.AssetPlugin,
						 octoprint.plugin.TemplatePlugin,
						 octoprint.plugin.StartupPlugin,
						 octoprint.plugin.ShutdownPlugin):
	def __init__(self):
		self.serial = None

	def open_serial_port(self, port, baud):
		self._logger.info('Opening serial port {}'.format(port))
		self.serial = serial.Serial()
		self.serial.baudrate = baud
		self.serial.port = port
		try:
			self.serial.open()
		except Exception as e:
			self._logger.warn('Error opening {} : {}'.format(port, e))

	##~~ SettingsPlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			port=None,
			ports=comm.serialList(),
			baud=115200,
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

	def on_settings_save(self, data):
		old_port = self._settings.get(['port'])
		old_baud = self._settings.get(['baud'])
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		new_port = self._settings.get(['port'])
		new_baud = self._settings.get(['baud'])
		if new_port != old_port or new_baud != old_baud:
			self._logger.info('Updating serial port {} : baud {}'.format(new_port, new_baud))
			self.open_serial_port(new_port, new_baud)

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
				displayName="PanTilt-Nano Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="you",
				repo="OctoPrint-PanTilt-Nano",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/you/OctoPrint-PantTilt-Nano/archive/{target_version}.zip"
			)
		)

	##~~ StartupPlugin

	def on_after_startup(self):
		self.open_serial_port(self._settings.get(['port']), self._settings.get(['baud']))

	##~~ ShutdownPlugin

	def on_shutdown(self):
		self._logger.info("Closing serial port {}".format(self._settings.get(['port'])))
		self.serial.close()

	##~~ pantilt command handler hook

	def handle_pantilt(self, values, **kwargs):
		pan = int(values['pan'])
		panMin = int(values['panMin'])
		panMax = int(values['panMax'])
		tilt = int(values['tilt'])
		tiltMin = int(values['tiltMin'])
		tiltMax = int(values['tiltMax'])

		# determine pan and tilt Us values
		panVal = (pan / (panMax - panMin)) * (
			(int(self._settings.get(["pan", "maxUs"])) - int(self._settings.get(["pan", "minUs"])))) + int(
			self._settings.get(
				["pan", "minUs"]))
		tiltVal = (tilt / (tiltMax - tiltMin)) * (
			(int(self._settings.get(["tilt", "maxUs"])) - int(self._settings.get(["tilt", "minUs"])))) + int(
			self._settings.get(
				["tilt", "minUs"]))

		if self.serial is not None and self.serial.isOpen():
			self.serial.write('setUs {} {}\n'.format(int(panVal), int(tiltVal)))
			self.serial.flush()
			# read the response
			self._logger.info(self.serial.readline())


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Pantilt_nanoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.plugin.pantilt_handler": __plugin_implementation__.handle_pantilt
	}
