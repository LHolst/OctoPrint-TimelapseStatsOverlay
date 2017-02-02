# coding=utf-8
from __future__ import absolute_import

from octoprint.plugin import (  EventHandlerPlugin,
                                SettingsPlugin,
                                StartupPlugin )
from octoprint.events import Events

from PIL import Image, ImageDraw, ImageFont

class TimelapseStatsOverlayPlugin(  EventHandlerPlugin,
                                    SettingsPlugin,
                                    StartupPlugin ):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            TimelapseStatsOverlay=dict(
                displayName="TimelapseStatsOverlay Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="LHolst",
                repo="OctoPrint-TimelapseStatsOverlay",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/LHolst/OctoPrint-TimelapseStatsOverlay/archive/{target_version}.zip"
            )
        )

    font = ImageFont.truetype('LiberationMono-Regular.ttf', 40)
    def on_after_startup(self):
            self._logger.info("Starting TimelapseStatsOverlay Plugin    Hi!")

    def on_event(self, event, payload):
        if event == Events.CAPTURE_DONE:
            self._logger.debug("Got event: {} with payload: {}".format(event, payload))
            self._handleCaptureDone(payload['file'])

    def _handleCaptureDone(self, file):
        current_progress = self._printer.get_current_data()['progress']
        self._logger.info("Handling Capture {}, completion {}".format(file, current_progress['completion']))
        frame = Image.open(file)
        width, height = frame.size
        self._logger.debug("Frame width: {} ,height: {}".format(width, height))
        draw = ImageDraw.Draw(frame)
        if current_progress['completion']:
            self._logger.debug("Drawing completion")
            draw.text((width/2, height/2), "P: {}%".format(current_progress['completion']*100), font=self.font, fill=(125, 125, 125, 255))
        if current_progress['printTime']:
            self._logger.debug("Drawing printTime")
            draw.text((width/2, height/4), "T: {}%".format(current_progress['printTime']), font=self.font, fill=(125, 125, 125, 255))
        del draw
        frame.save(file)
        self._logger.debug("Frame saved")

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "TimelapseStatsOverlay"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TimelapseStatsOverlayPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

