# 🚀 Space Trajectory Simulator

A desktop application to simulate **projectile motion in space
environments**.\
Built with **Python (Tkinter + Matplotlib)** and packaged as a
standalone executable using **PyInstaller**.

## 📂 Project Structure

    ├── dist/
    │   └── main.exe        # Executable file (ready to run, no Python required)
    ├── main.py             # Source code (Tkinter + Matplotlib)
    ├── main.spec           # PyInstaller build spec
    ├── .gitattributes
    └── README.md

## ✨ Features

-   Input **velocity, angle, gravity, and initial height**\
-   Predefined gravity for **Earth 🌍, Moon 🌕, and Mars ♂️**\
-   Displays:
    -   🕒 Time of flight\
    -   🔼 Maximum height\
    -   ➡ Horizontal range\
-   Interactive **trajectory plot** (with max height and landing point
    markers)\
-   Modern **dark-space GUI theme**

## ▶️ How to Run

### Option 1: Run the EXE (no Python required)

1.  Go to the `dist` folder.\
2.  Double-click **`main.exe`** to launch the simulator.

### Option 2: Run from Source (requires Python)

1.  Install dependencies:

    ``` bash
    pip install matplotlib
    ```

    *(Tkinter is included with standard Python installations)*

2.  Run the app:

    ``` bash
    python main.py
    ```

## 🖼 Preview

The app opens a **GUI window** with: - Input panel (velocity, angle,
gravity, height, planet selector)\
- Results panel\
- Live matplotlib trajectory plot

## 🛠 Build Instructions (for developers)

To rebuild the executable with PyInstaller:

``` bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```

This generates `dist/main.exe`.

## 📜 License

This project is for **educational purposes** and free to use.
