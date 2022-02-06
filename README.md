# SWui
A program for users emulating the mobile game Summoners War on NoxPlayer.

This tool calculates the current and maximum efficiency of any rune on screen, and outputs the info in a side window.

![image](https://user-images.githubusercontent.com/61902949/152680976-bc1c9138-3b93-4831-8b7c-5dd78b002610.png)

It first searches for any boxes (green rectangle in above image) on the emulator screen. Then it uses Tesseract's optical character recognition (OCR) engine to parse the data in input boxes. This data is then used to calculate current and maximum efficiency. Formula and weights are identical to the defaults in Xzandro's Summoners War Optimizer.

## Installing and Running
**Requirements:**
- at least Python 3.7
- Tesseract 5.0.0.x ([5.0.0.x -> Binaries](https://github.com/tesseract-ocr/tessdoc))

**Installing:**
1. Clone or download the repository
    ```
    git clone https://github.com/ghuang582/SWOverlay
    ```
2. Install required Python libraries using requirements.txt. Make sure your terminal is in the directory of the cloned repository.

    **Windows**
    ```
    py -m pip install -r requirements.txt
    ```
    
    **Unix/macOS**
    ```
    python -m pip install -r requirements.txt
    ```
3. Configure settings in config.py with an editor. You may need to change:
    - ```window_name``` to the name of your emulator (currently only tested on NoxPlayer)
    - ```pytesseract_path``` and redirect the path to where you installed Tesseract
    
**Running:**
```
python run.py
```


