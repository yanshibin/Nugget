from PySide6 import QtCore, QtWidgets
from enum import Enum
import webbrowser
import plistlib

from pymobiledevice3.lockdown import create_using_usbmux

from qt.ui_mainwindow import Ui_Nugget

from devicemanagement.constants import Version
from devicemanagement.device_manager import DeviceManager

from gui.gestalt_dialog import GestaltDialog

from tweaks.tweaks import tweaks

class Page(Enum):
    Home = 0
    Gestalt = 1
    FeatureFlags = 2
    EUEnabler = 3
    Springboard = 4
    InternalOptions = 5
    Apply = 6
    Settings = 7

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, device_manager: DeviceManager):
        super(MainWindow, self).__init__()
        self.device_manager = device_manager
        self.ui = Ui_Nugget()
        self.ui.setupUi(self)
        self.show_uuid = False
        self.loadSettings()

        ## DEVICE BAR
        self.refresh_devices()

        self.ui.refreshBtn.clicked.connect(self.refresh_devices)
        self.ui.devicePicker.currentIndexChanged.connect(self.change_selected_device)

        ## SIDE BAR ACTIONS
        self.ui.homePageBtn.clicked.connect(self.on_homePageBtn_clicked)
        self.ui.gestaltPageBtn.clicked.connect(self.on_gestaltPageBtn_clicked)
        self.ui.featureFlagsPageBtn.clicked.connect(self.on_featureFlagsPageBtn_clicked)
        self.ui.euEnablerPageBtn.clicked.connect(self.on_euEnablerPageBtn_clicked)
        self.ui.springboardOptionsPageBtn.clicked.connect(self.on_springboardOptionsPageBtn_clicked)
        self.ui.internalOptionsPageBtn.clicked.connect(self.on_internalOptionsPageBtn_clicked)
        self.ui.applyPageBtn.clicked.connect(self.on_applyPageBtn_clicked)
        self.ui.settingsPageBtn.clicked.connect(self.on_settingsPageBtn_clicked)

        ## HOME PAGE ACTIONS
        self.ui.phoneVersionLbl.linkActivated.connect(self.toggle_version_label)

        ## HOME PAGE LINKS
        self.ui.bigNuggetBtn.clicked.connect(self.on_bigNuggetBtn_clicked)
        self.ui.starOnGithubBtn.clicked.connect(self.on_githubBtn_clicked)

        self.ui.leminGithubBtn.clicked.connect(self.on_leminGitHubBtn_clicked)
        self.ui.leminTwitterBtn.clicked.connect(self.on_leminTwitterBtn_clicked)
        self.ui.leminKoFiBtn.clicked.connect(self.on_leminKoFiBtn_clicked)
        
        self.ui.jjtechBtn.clicked.connect(self.on_jjtechBtn_clicked)
        self.ui.disfordottieBtn.clicked.connect(self.on_disfordottieBtn_clicked)
        self.ui.lrdsnowBtn.clicked.connect(self.on_lrdsnowBtn_clicked)

        self.ui.libiBtn.clicked.connect(self.on_libiBtn_clicked)
        self.ui.qtBtn.clicked.connect(self.on_qtBtn_clicked)

        self.ui.discordBtn.clicked.connect(self.on_discordBtn_clicked)

        ## ELIGIBILITY PAGE ACTIONS
        self.ui.euEnablerEnabledChk.toggled.connect(self.on_euEnablerEnabledChk_toggled)
        self.ui.methodChoiceDrp.activated.connect(self.on_methodChoiceDrp_activated)
        self.ui.regionCodeTxt.textEdited.connect(self.on_regionCodeTxt_textEdited)

        self.ui.enableAIChk.toggled.connect(self.on_enableAIChk_toggled)
        self.ui.languageTxt.textEdited.connect(self.on_languageTxt_textEdited)
        self.ui.spoofModelChk.toggled.connect(self.on_spoofModelChk_toggled)

        ## FEATURE FLAGS PAGE
        self.ui.clockAnimChk.toggled.connect(self.on_clockAnimChk_toggled)
        self.ui.lockscreenChk.toggled.connect(self.on_lockscreenChk_clicked)
        self.ui.photosChk.toggled.connect(self.on_photosChk_clicked)
        self.ui.aiChk.toggled.connect(self.on_aiChk_clicked)

        ## SPRINGBOARD OPTIONS PAGE ACTIONS
        self.ui.footnoteTxt.textEdited.connect(self.on_footnoteTxt_textEdited)
        self.ui.disableLockRespringChk.toggled.connect(self.on_disableLockRespringChk_clicked)
        self.ui.disableDimmingChk.toggled.connect(self.on_disableDimmingChk_clicked)
        self.ui.disableBatteryAlertsChk.toggled.connect(self.on_disableBatteryAlertsChk_clicked)
        self.ui.disableCrumbChk.toggled.connect(self.on_disableCrumbChk_clicked)
        self.ui.enableSupervisionTextChk.toggled.connect(self.on_enableSupervisionTextChk_clicked)
        self.ui.enableAirPlayChk.toggled.connect(self.on_enableAirPlayChk_clicked)

        ## INTERNAL OPTIONS PAGE ACTIONS
        self.ui.buildVersionChk.toggled.connect(self.on_buildVersionChk_clicked)
        self.ui.RTLChk.toggled.connect(self.on_RTLChk_clicked)
        self.ui.metalHUDChk.toggled.connect(self.on_metalHUDChk_clicked)
        self.ui.accessoryChk.toggled.connect(self.on_accessoryChk_clicked)
        self.ui.iMessageChk.toggled.connect(self.on_iMessageChk_clicked)
        self.ui.IDSChk.toggled.connect(self.on_IDSChk_clicked)
        self.ui.VCChk.toggled.connect(self.on_VCChk_clicked)
        self.ui.appStoreChk.toggled.connect(self.on_appStoreChk_clicked)
        self.ui.notesChk.toggled.connect(self.on_notesChk_clicked)
        self.ui.showTouchesChk.toggled.connect(self.on_showTouchesChk_clicked)
        self.ui.hideRespringChk.toggled.connect(self.on_hideRespringChk_clicked)
        self.ui.enableWakeVibrateChk.toggled.connect(self.on_enableWakeVibrateChk_clicked)
        self.ui.pasteSoundChk.toggled.connect(self.on_pasteSoundChk_clicked)
        self.ui.notifyPastesChk.toggled.connect(self.on_notifyPastesChk_clicked)

        ## APPLY PAGE ACTIONS
        self.ui.applyTweaksBtn.clicked.connect(self.on_applyPageBtn_clicked)
        self.ui.removeTweaksBtn.clicked.connect(self.on_removeTweaksBtn_clicked)
        self.ui.chooseGestaltBtn.clicked.connect(self.on_chooseGestaltBtn_clicked)
        self.ui.resetGestaltBtn.clicked.connect(self.on_resetGestaltBtn_clicked)

        ## MOBILE GESTALT PAGE ACTIONS
        self.ui.dynamicIslandDrp.activated.connect(self.on_dynamicIslandDrp_activated)
        self.ui.rdarFixChk.clicked.connect(self.on_rdarFixChk_clicked)
        self.ui.modelNameChk.toggled.connect(self.on_modelNameChk_clicked)
        self.ui.modelNameTxt.textEdited.connect(self.on_modelNameTxt_textEdited)

        self.ui.bootChimeChk.clicked.connect(self.on_bootChimeChk_clicked)
        self.ui.chargeLimitChk.clicked.connect(self.on_chargeLimitChk_clicked)
        self.ui.tapToWakeChk.clicked.connect(self.on_tapToWakeChk_clicked)
        self.ui.iphone16SettingsChk.clicked.connect(self.on_iphone16SettingsChk_clicked)
        self.ui.parallaxChk.clicked.connect(self.on_parallaxChk_clicked)
        self.ui.stageManagerChk.clicked.connect(self.on_stageManagerChk_clicked)
        self.ui.enableMedusaChk.clicked.connect(self.on_enableMedusaChk_clicked)
        self.ui.ipadAppsChk.clicked.connect(self.on_ipadAppsChk_clicked)
        self.ui.shutterChk.clicked.connect(self.on_shutterChk_clicked)
        self.ui.findMyFriendsChk.clicked.connect(self.on_findMyFriendsChk_clicked)
        self.ui.pencilChk.clicked.connect(self.on_pencilChk_clicked)
        self.ui.actionButtonChk.clicked.connect(self.on_actionButtonChk_clicked)

        self.ui.internalInstallChk.clicked.connect(self.on_internalInstallChk_clicked)
        self.ui.internalStorageChk.clicked.connect(self.on_internalStorageChk_clicked)
        self.ui.collisionSOSChk.clicked.connect(self.on_collisionSOSChk_clicked)
        self.ui.aodChk.clicked.connect(self.on_aodChk_clicked)
        self.ui.sleepApneaChk.clicked.connect(self.on_sleepApneaChk_clicked)


    ## GENERAL INTERFACE FUNCTIONS
    def updateInterfaceForNewDevice(self):
        # update the home page
        self.updatePhoneInfo()


    ## DEVICE BAR FUNCTIONS
    @QtCore.Slot()
    def refresh_devices(self):
        # get the devices
        self.device_manager.get_devices()
        # clear the picker
        self.ui.devicePicker.clear()
        self.ui.restoreProgressBar.hide()
        if len(self.device_manager.devices) == 0:
            self.ui.devicePicker.setEnabled(False)
            self.ui.devicePicker.addItem('None')
            self.ui.pages.setCurrentIndex(Page.Home.value)
            self.ui.homePageBtn.setChecked(True)

            # hide all pages
            self.ui.explorePageBtn.hide()
            self.ui.locSimPageBtn.hide()
            self.ui.sidebarDiv1.hide()

            self.ui.gestaltPageBtn.hide()
            self.ui.featureFlagsPageBtn.hide()
            self.ui.euEnablerPageBtn.hide()
            self.ui.springboardOptionsPageBtn.hide()
            self.ui.internalOptionsPageBtn.hide()

            self.ui.sidebarDiv2.hide()
            self.ui.applyPageBtn.hide()
        else:
            self.ui.devicePicker.setEnabled(True)
            # populate the ComboBox with device names
            for device in self.device_manager.devices:
                self.ui.devicePicker.addItem(device.name)
            
            # show all pages
            self.ui.explorePageBtn.hide()
            self.ui.locSimPageBtn.hide()
            self.ui.sidebarDiv1.show()
            self.ui.gestaltPageBtn.show()
            # self.ui.featureFlagsPageBtn.show()
            self.ui.euEnablerPageBtn.show()
            self.ui.springboardOptionsPageBtn.show()
            self.ui.internalOptionsPageBtn.show()
            
            self.ui.sidebarDiv2.show()
            self.ui.applyPageBtn.show()

            self.ui.gestaltPageContent.setDisabled(False)
            self.ui.featureFlagsPageContent.setDisabled(False)
            self.ui.euEnablerPageContent.setDisabled(False)
            self.ui.springboardOptionsPageContent.setDisabled(False)
            self.ui.internalOptionsPageContent.setDisabled(False)
        
        # update the selected device
        self.ui.devicePicker.setCurrentIndex(0)
        self.change_selected_device(0)

        # update the interface
        self.updateInterfaceForNewDevice()

    def change_selected_device(self, index):
        if len(self.device_manager.devices) > 0:
            self.device_manager.set_current_device(index=index)
            # hide options that are for newer versions
            # remove the new dynamic island options
            try:
                self.ui.dynamicIslandDrp.removeItem(6)
                self.ui.dynamicIslandDrp.removeItem(5)
            except:
                pass
            rdar_title = tweaks["RdarFix"].get_rdar_title()
            if rdar_title == "hide":
                self.ui.rdarFixChk.hide()
            else:
                self.ui.rdarFixChk.show()
                self.ui.rdarFixChk.setText(f"{rdar_title} (modifies resolution)")
            if Version(self.device_manager.data_singleton.current_device.version) >= Version("18.1"):
                self.ui.enableAIChk.show()
                self.ui.languageLbl.hide()
                self.ui.languageTxt.hide()
                self.ui.aiInfoLabel.hide()
                self.ui.spoofModelChk.hide()
            else:
                self.ui.enableAIChk.hide()
                self.ui.languageLbl.hide()
                self.ui.languageTxt.hide()
                self.ui.aiInfoLabel.hide()
                self.ui.spoofModelChk.hide()
            if Version(self.device_manager.data_singleton.current_device.version) >= Version("18.0"):
                self.ui.aodChk.show()
                self.ui.iphone16SettingsChk.show()
                self.ui.sleepApneaChk.show()
                self.ui.featureFlagsPageBtn.show()
                # show the other dynamic island options
                self.ui.dynamicIslandDrp.addItem("2622 (iPhone 16 Pro Dynamic Island)")
                self.ui.dynamicIslandDrp.addItem("2868 (iPhone 16 Pro Max Dynamic Island)")
            else:
                self.ui.aodChk.hide()
                self.ui.iphone16SettingsChk.hide()
                self.ui.sleepApneaChk.hide()
                self.ui.featureFlagsPageBtn.hide()
        else:
            self.device_manager.set_current_device(index=None)
            self.ui.featureFlagsPageBtn.hide()

    def loadSettings(self):
        self.settings = QtCore.QSettings()
        try:
            # load the settings
            apply_over_wifi = self.settings.value("apply_over_wifi", True, type=bool)
            self.ui.allowWifiApplyingChk.setChecked(apply_over_wifi)
            self.device_manager.apply_over_wifi = apply_over_wifi
        except:
            pass
    

    ## SIDE BAR FUNCTIONS
    def on_homePageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.Home.value)
    
    def on_gestaltPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.Gestalt.value)

    def on_featureFlagsPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.FeatureFlags.value)
    
    def on_euEnablerPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.EUEnabler.value)

    def on_springboardOptionsPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.Springboard.value)

    def on_internalOptionsPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.InternalOptions.value)

    def on_applyPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.Apply.value)

    def on_settingsPageBtn_clicked(self):
        self.ui.pages.setCurrentIndex(Page.Settings.value)

    def update_side_btn_color(self, btn: QtWidgets.QToolButton, toggled: bool):
        if toggled:
            btn.setStyleSheet("QToolButton {\ncolor: #00FF00;\n}")
        else:
            btn.setStyleSheet("")
    

    ## HOME PAGE
    def updatePhoneInfo(self):
        # name label
        self.ui.phoneNameLbl.setText(self.device_manager.get_current_device_name())
        # version label
        ver = self.device_manager.get_current_device_version()
        self.show_uuid = False
        if ver != "":
            self.show_version_text(version=ver)
        else:
            self.ui.phoneVersionLbl.setText("Please connect a device.")

    def toggle_version_label(self):
        if self.show_uuid:
            self.show_uuid = False
            ver = self.device_manager.get_current_device_version()
            if ver != "":
                self.show_version_text(version=ver)
        else:
            self.show_uuid = True
            uuid = self.device_manager.get_current_device_uuid()
            if uuid != "":
                self.ui.phoneVersionLbl.setText(f"<a style=\"text-decoration:none; color: white\" href=\"#\">{uuid}</a>")

    def show_version_text(self, version: str):
        support_str: str = "<span style=\"color: #32d74b;\">Supported!</span></a>"
        if not self.device_manager.get_current_device_supported():
            support_str = "<span style=\"color: #ff0000;\">Not Supported.</span></a>"
        self.ui.phoneVersionLbl.setText(f"<a style=\"text-decoration:none; color: white;\" href=\"#\">iOS {version} {support_str}")

    ## HOME PAGE LINKS
    def on_bigMilkBtn_clicked(self):
        webbrowser.open_new_tab("https://cowabun.ga")

    def on_leminGitHubBtn_clicked(self):
        webbrowser.open_new_tab("https://github.com/leminlimez")
    def on_leminTwitterBtn_clicked(self):
        webbrowser.open_new_tab("https://twitter.com/LeminLimez")
    def on_leminKoFiBtn_clicked(self):
        webbrowser.open_new_tab("https://ko-fi.com/leminlimez")

    def on_jjtechBtn_clicked(self):
        webbrowser.open_new_tab("https://github.com/JJTech0130/TrollRestore")
    def on_disfordottieBtn_clicked(self):
        webbrowser.open_new_tab("https://twitter.com/disfordottie")
    def on_lrdsnowBtn_clicked(self):
        webbrowser.open_new_tab("https://github.com/Lrdsnow/EUEnabler")

    def on_libiBtn_clicked(self):
        webbrowser.open_new_tab("https://github.com/doronz88/pymobiledevice3")
    def on_qtBtn_clicked(self):
        webbrowser.open_new_tab("https://www.qt.io/product/development-tools")

    def on_discordBtn_clicked(self):
        webbrowser.open_new_tab("https://discord.gg/MN8JgqSAqT")
    def on_githubBtn_clicked(self):
        webbrowser.open_new_tab("https://github.com/leminlimez/Nugget")
    def on_bigNuggetBtn_clicked(self):
        webbrowser.open_new_tab("https://cowabun.ga")


    ## MOBILE GESTALT PAGE
    def on_dynamicIslandDrp_activated(self, index: int):
        if index == 0:
            tweaks["DynamicIsland"].set_enabled(False)
        else:
            tweaks["DynamicIsland"].set_selected_option(index - 1)
            tweaks["RdarFix"].set_di_type(tweaks["DynamicIsland"].value[tweaks["DynamicIsland"].get_selected_option()])
    def on_rdarFixChk_clicked(self, checked: bool):
        tweaks["RdarFix"].set_enabled(checked)

    def on_modelNameChk_clicked(self, checked: bool):
        tweaks["ModelName"].set_enabled(checked)
    def on_modelNameTxt_textEdited(self, text: str):
        tweaks["ModelName"].set_value(text, toggle_enabled=False)

    def on_bootChimeChk_clicked(self, checked: bool):
        tweaks["BootChime"].set_enabled(checked)
    def on_chargeLimitChk_clicked(self, checked: bool):
        tweaks["ChargeLimit"].set_enabled(checked)
    def on_tapToWakeChk_clicked(self, checked: bool):
        tweaks["TapToWake"].set_enabled(checked)
    def on_iphone16SettingsChk_clicked(self, checked: bool):
        tweaks["CameraButton"].set_enabled(checked)
    def on_parallaxChk_clicked(self, checked: bool):
        tweaks["Parallax"].set_enabled(checked)

    def on_stageManagerChk_clicked(self, checked: bool):
        tweaks["StageManager"].set_enabled(checked)
    def on_enableMedusaChk_clicked(self, checked: bool):
        tweaks["Medusa"].set_enabled(checked)
    def on_ipadAppsChk_clicked(self, checked: bool):
        tweaks["iPadApps"].set_enabled(checked)
    def on_shutterChk_clicked(self, checked: bool):
        # TODO: allow the user to select the region
        tweaks["Shutter"].set_enabled(checked)
    def on_findMyFriendsChk_clicked(self, checked: bool):
        tweaks["FindMyFriends"].set_enabled(checked)
    def on_pencilChk_clicked(self, checked: bool):
        tweaks["Pencil"].set_enabled(checked)
    def on_actionButtonChk_clicked(self, checked: bool):
        tweaks["ActionButton"].set_enabled(checked)

    def on_internalInstallChk_clicked(self, checked: bool):
        tweaks["InternalInstall"].set_enabled(checked)
    def on_internalStorageChk_clicked(self, checked: bool):
        tweaks["InternalStorage"].set_enabled(checked)

    def on_collisionSOSChk_clicked(self, checked: bool):
        tweaks["CollisionSOS"].set_enabled(checked)
    def on_aodChk_clicked(self, checked: bool):
        tweaks["AOD"].set_enabled(checked)
    def on_sleepApneaChk_clicked(self, checked: bool):
        tweaks["SleepApnea"].set_enabled(checked)

    
    ## FEATURE FLAGS PAGE
    def on_clockAnimChk_toggled(self, checked: bool):
        tweaks["ClockAnim"].set_enabled(checked)
    def on_lockscreenChk_clicked(self, checked: bool):
        tweaks["Lockscreen"].set_enabled(checked)

    def on_photosChk_clicked(self, checked: bool):
        tweaks["PhotoUI"].set_enabled(checked)
    def on_aiChk_clicked(self, checked: bool):
        tweaks["AI"].set_enabled(checked)


    ## ELIGIBILITY PAGE
    def on_euEnablerEnabledChk_toggled(self, checked: bool):
        tweaks["EUEnabler"].set_enabled(checked)
    def on_methodChoiceDrp_activated(self, index: int):
        tweaks["EUEnabler"].set_selected_option(index)
    def on_regionCodeTxt_textEdited(self, text: str):
        tweaks["EUEnabler"].set_region_code(text)

    def on_enableAIChk_toggled(self, checked: bool):
        tweaks["AIEligibility"].set_enabled(checked)
        tweaks["AIGestalt"].set_enabled(checked)
        # change the visibility of stuff
        if checked:
            self.ui.languageLbl.show()
            self.ui.languageTxt.show()
            self.ui.aiInfoLabel.show()
            self.ui.spoofModelChk.show()
        else:
            self.ui.languageLbl.hide()
            self.ui.languageTxt.hide()
            self.ui.aiInfoLabel.hide()
            self.ui.spoofModelChk.hide()
    def on_languageTxt_textEdited(self, text: str):
        tweaks["AIEligibility"].set_language_code(text)
    def on_spoofModelChk_toggled(self, checked: bool):
        tweaks["SpoofModel"].set_enabled(checked)


    ## SPRINGBOARD OPTIONS PAGE
    def on_footnoteTxt_textEdited(self, text: str):
        tweaks["LockScreenFootnote"].set_value(text, toggle_enabled=True)

    def on_disableLockRespringChk_clicked(self, checked: bool):
        tweaks["SBDontLockAfterCrash"].set_enabled(checked)
    def on_disableBatteryAlertsChk_clicked(self, checked: bool):
        tweaks["SBDontDimOrLockOnAC"].set_enabled(checked)
    def on_disableDimmingChk_clicked(self, checked: bool):
        tweaks["SBHideLowPowerAlerts"].set_enabled(checked)
    def on_disableCrumbChk_clicked(self, checked: bool):
        tweaks["SBNeverBreadcrumb"].set_enabled(checked)
    def on_enableSupervisionTextChk_clicked(self, checked: bool):
        tweaks["SBShowSupervisionTextOnLockScreen"].set_enabled(checked)
    def on_enableAirPlayChk_clicked(self, checked: bool):
        tweaks["AirplaySupport"].set_enabled(checked)

    
    ## INTERNAL OPTIONS PAGE
    def on_buildVersionChk_clicked(self, checked: bool):
        tweaks["SBBuildNumber"].set_enabled(checked)
    def on_RTLChk_clicked(self, checked: bool):
        tweaks["RTL"].set_enabled(checked)
    def on_metalHUDChk_clicked(self, checked: bool):
        tweaks["MetalForceHudEnabled"].set_enabled(checked)
    def on_accessoryChk_clicked(self, checked: bool):
        tweaks["AccessoryDeveloperEnabled"].set_enabled(checked)
    def on_iMessageChk_clicked(self, checked: bool):
        tweaks["iMessageDiagnosticsEnabled"].set_enabled(checked)
    def on_IDSChk_clicked(self, checked: bool):
        tweaks["IDSDiagnosticsEnabled"].set_enabled(checked)
    def on_VCChk_clicked(self, checked: bool):
        tweaks["VCDiagnosticsEnabled"].set_enabled(checked)

    def on_appStoreChk_clicked(self, checked: bool):
        tweaks["AppStoreDebug"].set_enabled(checked)
    def on_notesChk_clicked(self, checked: bool):
        tweaks["NotesDebugMode"].set_enabled(checked)

    def on_showTouchesChk_clicked(self, checked: bool):
        tweaks["BKDigitizerVisualizeTouches"].set_enabled(checked)
    def on_hideRespringChk_clicked(self, checked: bool):
        tweaks["BKHideAppleLogoOnLaunch"].set_enabled(checked)
    def on_enableWakeVibrateChk_clicked(self, checked: bool):
        tweaks["EnableWakeGestureHaptic"].set_enabled(checked)
    def on_pasteSoundChk_clicked(self, checked: bool):
        tweaks["PlaySoundOnPaste"].set_enabled(checked)
    def on_notifyPastesChk_clicked(self, checked: bool):
        tweaks["AnnounceAllPastes"].set_enabled(checked)

    
    ## SETTINGS PAGE
    def on_allowWifiApplyingChk_toggled(self, checked: bool):
        self.device_manager.apply_over_wifi = checked
        # save the setting
        self.settings.setValue("apply_over_wifi", checked)


    ## APPLY PAGE
    def on_chooseGestaltBtn_clicked(self):
        selected_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Mobile Gestalt File", "", "Plist Files (*.plist)", options=QtWidgets.QFileDialog.ReadOnly)
        if selected_file == "" or selected_file == None:
            self.device_manager.data_singleton.gestalt_path = None
            self.ui.gestaltLocationLbl.setText("None")
        else:
            # verify that the gestalt is correct and compatible
            with open(selected_file, 'rb') as in_fp:
                gestalt_plist = plistlib.load(in_fp)
            if not "CacheExtra" in gestalt_plist:
                detailsBox = QtWidgets.QMessageBox()
                detailsBox.setIcon(QtWidgets.QMessageBox.Critical)
                detailsBox.setWindowTitle("Error!")
                detailsBox.setText("The file is not a mobile gestalt file!")
                detailsBox.exec()
                return
            if (
                not "qNNddlUK+B/YlooNoymwgA" in gestalt_plist["CacheExtra"]
                or gestalt_plist["CacheExtra"]["qNNddlUK+B/YlooNoymwgA"] != self.device_manager.data_singleton.current_device.version
                or gestalt_plist["CacheExtra"]["0+nc/Udy4WNG8S+Q7a/s1A"] != self.device_manager.data_singleton.current_device.model
                or not "0+nc/Udy4WNG8S+Q7a/s1A" in gestalt_plist["CacheExtra"]
            ):
                dialog = GestaltDialog(
                        device_manager=self.device_manager,
                        gestalt_label=self.ui.gestaltLocationLbl,
                        selected_file=selected_file
                    )
                dialog.exec()
            self.device_manager.data_singleton.gestalt_path = selected_file
            self.ui.gestaltLocationLbl.setText(selected_file)

    def update_label(self, txt: str):
        self.ui.statusLbl.setText(txt)
    def update_bar(self, percent):
        self.ui.restoreProgressBar.setValue(int(percent))
    def on_removeTweaksBtn_clicked(self):
        # TODO: Add safety here
        self.device_manager.apply_changes(resetting=True, update_label=self.update_label)
    def on_resetGestaltBtn_clicked(self):
        self.device_manager.reset_mobilegestalt(update_label=self.update_label)

    @QtCore.Slot()
    def on_applyTweaksBtn_clicked(self):
        # TODO: Add safety here
        self.device_manager.apply_changes(update_label=self.update_label)
