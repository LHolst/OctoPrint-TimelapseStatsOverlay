# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

from octoprint.plugin import AssetPlugin, EventHandlerPlugin, TemplatePlugin
from octoprint.events import Events
from PIL import Image, ImageDraw, ImageFont

class TimelapseStatsOverlayPlugin(SettingsPlugin, AssetPlugin, TemplatePlugin):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/TimelapseStatsOverlay.js"],
            css=["css/TimelapseStatsOverlay.css"],
            less=["less/TimelapseStatsOverlay.less"]
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
    def on_event(self, event, payload):
        if event == Events.CAPTURE_DONE:
            self._handleCaptureDone(payload['file'])

    def _handleCaptureDone(self, file):
        current_progress = self._printer.get_current_data()['progress']
        self._logger.info("Handling Capture {}, completion {}".format(file, current_progress['completion']))
        frame = Image.open(file)
        width, height = frame.size
        draw = ImageDraw.Draw(frame)
        if current_progress['completion']:
                draw.text((width/2, height/2), "P: {}%".format(current_progress['completion']*100), font=self.font, fill=(125, 125, 125, 255))
        if current_progress['printTime']:
                draw.text((width/2, height/4), "T: {}%".format(current_progress['printTime']), font=self.font, fill=(125, 125, 125, 255))
        del draw
            frame.save(file)

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "TimelapseStatsOverlay Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TimelapseStatsOverlayPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

