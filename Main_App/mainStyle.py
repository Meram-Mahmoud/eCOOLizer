darkColor = "#121212"
yellowColor = "#F7D800"
fontFamily = "Roboto, sans-serif"

mainStyle = f"""
    QMainWindow {{
        background-color: {darkColor};
    }}
"""
logoStyle = f"""
    QLabel{{
        font-family: "LEMON MILK";
        font-size:22px;
        font-weight:600;
        color:{yellowColor};
    }}
"""
audioNameStyle = f"""
    QLabel{{
        font-family:{fontFamily};
        font-size:14px;
        font-weight:500;
        color:"#EFEFEF";
    }}
"""
importButton =f"""
    QPushButton{{  
        background-color: {yellowColor};
        color:{darkColor};
        border-radius: 5px;
        padding:7px;
        font-family:{fontFamily};
        font-size:12px;
        font-weight:600;
    }}
"""
buttonsGroupStyle = f"""
    QWidget {{
        background-color: {yellowColor};
        border-radius: 19px;
        border:0;
        padding:0;
    }}
"""
buttonStyle = f"""
    QPushButton {{
        background-color: none;
        border: none;
        margin: 0; 
        padding: 0;
    }}
"""
controlButtonStyle = f"""
    QPushButton {{
        background-color: {yellowColor};
        width:50px;
        border: 1px solid {yellowColor};
        border-radius:13px;
        margin: 0; 
        padding: 2px;
    }}
"""

sliderStyle = f"""
    QSlider::groove:vertical {{
        background: {darkColor};
        position: absolute; /* absolutely position 4px from the left and right of the widget */
        left: 8px; right: 8px;
    }}    

    QSlider::handle:vertical {{
        width: 15px;  /* Adjust the width and height to make it round */
        height: 15px;
        background: {yellowColor};
        border-radius: 1px;  /* Makes the handle circular */
        margin: 0 -25px;  /* Expand outside the groove */
    }}
    QSlider::add-page:vertical {{
        background: {yellowColor};
        width:10px;
    }}

    QSlider::sub-page:vertical {{
        background: #EFEFEF;
    }}
"""

sliderLabelStyle = f"""
    QLabel{{
        font-size:12px;
        font-weight:600;
        color:{yellowColor};
    }}
"""

speedSliderStyle = f"""
    QSlider::groove:horizontal {{
        background: {darkColor};
        height: 2px;  /* Smaller height for a sleeker appearance */
        border-radius: 2px;
        margin: 0px 12px; /* Adds space around the groove */
    }}

    QSlider::handle:horizontal {{
        background: {yellowColor};
        width: 15px;  /* Smaller width for a compact look */
        height: 15px;
        border-radius: 5px;  /* Round handle */
        margin: -3px 0px; /* Adjust handle position */
    }}

    QSlider::add-page:horizontal {{
        background: #EFEFEF;
        height: 2px;
        border-radius: 2px;
    }}

    QSlider::sub-page:horizontal {{
        background: {yellowColor};
        height: 2px;
        border-radius: 2px;
    }}
"""

radioButtonStyle = f"""
    QRadioButton {{
        color: {yellowColor};
        font-family: {fontFamily};
        font-size: 12px;
        font-weight: 500;
        spacing: 6px; /* Space between radio circle and label */
    }}

    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid {yellowColor};
        background-color: {darkColor};
    }}

    QRadioButton::indicator:checked {{
        background-color: {yellowColor};
        border: 2px solid {yellowColor};
    }}

    QRadioButton::indicator:hover {{
        border: 2px solid #FFFFFF; /* Lighten border on hover */
    }}
"""