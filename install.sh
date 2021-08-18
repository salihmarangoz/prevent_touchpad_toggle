
INSTALL_DIR="$HOME/.local/share"


mkdir -p $INSTALL_DIR/prevent_touchpad_toggle_app
cp prevent_touchpad_toggle_app.py $INSTALL_DIR/prevent_touchpad_toggle_app.py
cp touchpad.png $INSTALL_DIR/touchpad.png
cp README.md $INSTALL_DIR/README.md


tee $HOME/.config/autostart/prevent_touchpad_toggle_app.desktop << END
[Desktop Entry]
Type=Application
Exec=/usr/bin/python3 $INSTALL_DIR/prevent_touchpad_toggle_app.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=prevent_touchpad_toggle_app
Name=prevent_touchpad_toggle_app
Comment[en_US]=
Comment=
END

echo "Done!"