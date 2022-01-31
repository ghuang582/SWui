# SWOverlay
A program for users emulating the mobile game Summoners War on NoxPlayer.

This tool calculates the current and maximum efficiency of any rune on screen, and outputs the info in a side window.

It first searches for any boxes (rectangles) on the emulator screen. Then it uses Tesseract's optical character recognition (OCR) engine to parse the data in input boxes. This data is then used to calculate current and maximum efficiency. Formula and weights are identical to the defaults in Xzandro's Summoners War Optimizer.
