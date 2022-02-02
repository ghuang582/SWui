# SWOverlay
A program for users emulating the mobile game Summoners War on NoxPlayer.

This tool calculates the current and maximum efficiency of any rune on screen, and outputs the info in a side window.

![image](https://user-images.githubusercontent.com/61902949/152159171-aa3bf945-1234-4ae5-baf2-4b2c306ed194.png)

It first searches for any boxes (green rectangle in above image) on the emulator screen. Then it uses Tesseract's optical character recognition (OCR) engine to parse the data in input boxes. This data is then used to calculate current and maximum efficiency. Formula and weights are identical to the defaults in Xzandro's Summoners War Optimizer.
