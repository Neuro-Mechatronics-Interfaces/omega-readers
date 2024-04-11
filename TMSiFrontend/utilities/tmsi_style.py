'''
(c) 2024 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file tmsi_style.py
 * @brief 
 * TMSi style for the interface.
 */


'''
import os
from pkg_resources import resource_filename

# Get the path to the images directory
images_dir = resource_filename(__name__, '../media/images/')
images_dir = images_dir.replace("\\", "/")

if not os.path.exists(images_dir):
    # If it doesn't exist, try looking in the parent directory
    images_dir = resource_filename(__name__, '../../media/images/')
    images_dir = images_dir.replace("\\", "/")

TMSiStyle = '''
* {
    background: transparent;
    font-size: 12px;
}                                

QMainWindow {
    border-image: url(''' + images_dir + '''Achtergrond.png) 0 0 0 0 stretch stretch;
}

QMenu {
    background: white;
}

QPushButton { 
    background-color: white;
    border-style: solid; 
    border-radius: 14px;
    border-color:  #FC4C02;
    border-width: 4px;
    padding: 8px;
    color: black;
    min-width: 50px;
}

QPushButton:disabled { 
    background-color: #e6e6e6;
    border-color:  #d6d6d6;
    color: white;
}

QPushButton:hover {
    background-color: #FC4C02;
    color: white;
    font-weight: bold;
}

QRadioButton::indicator {
    width: 13px;
    height: 13px;
}

QRadioButton::indicator::unchecked {
        image: url(''' + images_dir + '''radiobutton_unchecked.png);
    }

QRadioButton::indicator::checked {
    image: url(''' + images_dir + '''radiobutton_checked.png);
}

QRadioButton::indicator:unchecked:hover {
    image: url(''' + images_dir + '''radiobutton_unchecked.png);
}

QRadioButton::indicator:unchecked:pressed {
    image: url(''' + images_dir + '''radiobutton_unchecked.png);
}

QRadioButton::indicator:checked:hover {
    image: url(''' + images_dir + '''radiobutton_checked.png);
}

QRadioButton::indicator:checked:pressed {
    image: url(''' + images_dir + '''radiobutton_checked.png);
}
QFrame {
    background: transparent;
}

QToolBar {
    background: transparent;
    border-right: 1px solid #E5E5E5;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FC4C02, stop:1 #FF8200);
    width: 18px;
    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 3px;
}

QGroupBox {
    font-weight: bold;
}

QComboBox {
    background: white;
    border: 1px solid #ced4da;
    border-radius: 15px;
    padding-left: 10px;
}

QComboBox::drop-down {
    border: 0px;
}

QComboBox::down-arrow {
    image: url(''' + images_dir + '''arrow_down.png);
    width: 12px;
    height: 12px;
    margin-right: 15px;
}

QComboBox::on {
    border: 1px solid #FF8200;
}

QComboBox QAbstractItemView {
    border: 1px solid darkgrey;
    selection-background-color: #FF8200;
}

QListView {
    border: 1px solid rgba(0, 0, 0, 10%);
    padding: 5px;
    outline: 0px;
}

QListView::item {
    padding-left: 10px;
}

QListView::item:hover {
    background-color: #FF8200;
}

QTableView::item { 
    border-bottom: 1px solid #999; 
    border-right: none; 
}

QHeaderView::section {
    border: none;  /* Remove the border */
    border-bottom: 1px solid #999; 
    padding: 0;    /* Remove any padding */
    margin: 0;     /* Remove any margin */
}

QScrollBar:vertical, QScrollBar:horizontal {
    background-color: #d6d6d6;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px #d6d6d6;
    border-radius: 4px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FC4C02, stop:1 #FF8200);;         
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:disabled, QScrollBar::handle:horizontal:disabled {
    background-color: #d6d6d6;
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 0px;
    border-image: url(''' + images_dir + '''arrow_up.png);        /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    margin: 3px 0px 3px 0px;
    border-image: url(''' + images_dir + '''arrow_left.png);        /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}


QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 0px;
    border-image: url(''' + images_dir + '''arrow_down.png);       /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal {
    margin: 0px 3px 0px 3px;
    border-image: url(''' + images_dir + '''arrow_right.png);       /* # <-------- */
    width: 10px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}


QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
    border-image: url(''' + images_dir + '''arrow_up.png);                  /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
    border-image: url(''' + images_dir + '''arrow_left.png);               /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on {
    border-image: url(''' + images_dir + '''arrow_right.png);               /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
    border-image: url(''' + images_dir + '''arrow_down.png);                /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
    background: none;
}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QDialog {
background: white;
}

QCheckBox {
spacing: 5px;
}

QCheckBox::indicator {
width: 13px;
height: 13px;
}

QCheckBox::indicator:unchecked {
image: url(''' + images_dir + '''checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:hover {
image: url(''' + images_dir + '''checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:pressed {
image: url(''' + images_dir + '''checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:disabled {
image: url(''' + images_dir + '''checkbox_unchecked_disabled.png);
}

QCheckBox::indicator:checked {
image: url(''' + images_dir + '''checkbox_checked.png);
}

QCheckBox::indicator:checked:hover {
image: url(''' + images_dir + '''checkbox_checked.png);
}

QCheckBox::indicator:checked:pressed {
image: url(''' + images_dir + '''checkbox_checked.png);
}

QCheckBox::indicator:checked:disabled {
image: url(''' + images_dir + '''checkbox_checked_disabled.png);
}


'''