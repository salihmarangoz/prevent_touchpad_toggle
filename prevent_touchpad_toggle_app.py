from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
import os
import threading
import time


############# GLOBAL PARAMETERS ###################
threading_delay = 0.25
remember_last_setting = False
enable_command = 'gsettings set org.gnome.desktop.peripherals.touchpad send-events enabled'  # CODE: 1
disable_command = 'gsettings set org.gnome.desktop.peripherals.touchpad send-events disabled' # CODE: 0
# APP DISABLED CODE: 2
###################################################


# Allow interrupting with ctrl+c
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class myThread(threading.Thread):
   def __init__(self, is_enabled=False, system_command=enable_command):
      threading.Thread.__init__(self)
      self.is_enabled = is_enabled
      self.system_command = system_command
      self.is_stop = False

      if os.path.isfile("last_state.txt"):
         last_state_f = open("last_state.txt", "r")
         lines = last_state_f.readlines()
         code = int(lines[0])
         if code == 0:
            self.system_command = disable_command
            self.is_enabled = True
         elif code == 1:
            self.system_command = enable_command
            self.is_enabled = True
         elif code == 2:
            self.is_enabled = False
         last_state_f.close()

      self.last_state_f = open("last_state.txt", "a")

   def enable_and_change_command(self, code):
      if code == 0:
         self.system_command = disable_command
      elif code == 1:
         self.system_command = enable_command
      self.is_enabled = True

      self.last_state_f.seek(0)
      self.last_state_f.truncate()
      self.last_state_f.writelines([str(code)+"\n"])
      self.last_state_f.flush()

   def disable(self):
      self.is_enabled = False
      self.last_state_f.seek(0)
      self.last_state_f.truncate()
      self.last_state_f.writelines(["2"+"\n"])
      self.last_state_f.flush()

   def stop(self):
      self.is_stop = True

   def run(self):
      while True:
         if self.is_enabled:
            os.system(self.system_command)
         if self.is_stop:
            break
         time.sleep(threading_delay)


thread = myThread()
thread.start()


app = QApplication([])
app.setQuitOnLastWindowClosed(False)
icon = QIcon("touchpad.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

menu = QMenu()

stop_app = QAction("Stop Forcing")
menu.addAction(stop_app)
exec("stop_app.triggered.connect(lambda: thread.disable() )")

keep_enabled_action = QAction("Keep Touchpad Enabled")
menu.addAction(keep_enabled_action)
exec("keep_enabled_action.triggered.connect(lambda: thread.enable_and_change_command(1) )")

keep_disabled_action = QAction("Keep Touchpad Disabled")
menu.addAction(keep_disabled_action)
exec("keep_disabled_action.triggered.connect(lambda: thread.enable_and_change_command(0) )")


menu.addSeparator() #================================================================

about = QAction("About")
project_webpage_url = "https://github.com/salihmarangoz/prevent_touchpad_toggle"
exec("about.triggered.connect(lambda: webbrowser.open(project_webpage_url) )")
menu.addAction(about)


def exit_confirmation():
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Question)
   msgBox.setText("Are you sure to exit?")
   msgBox.setWindowTitle("Prevent Touchpad Toggle App")
   msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Yes:
      app.quit()
      thread.stop()


# To quit the app
quit = QAction("Quit")
quit.triggered.connect(exit_confirmation)
menu.addAction(quit)


# Adding options to the System Tray
tray.setContextMenu(menu)
  
app.exec_()