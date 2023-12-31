# vn-text-capture
A project aimed at developing software that enables **interactive learning** of the Japanese language through the use of **Visual Novels**.

The project is intended for usage by the general public.

![Sample Image](https://github.com/SaitoGH/vn-text-capture/assets/42116722/04e67671-fe86-4c0c-bdf3-cb3c5d3dac7c)

## API-Used

- *Jisho [Search API](https://jisho.org/)*
- *PyTesseract [OCR](https://github.com/madmaze/pytesseract)*
- *GoogleTrans [Translation-JP-to-EN](https://github.com/ssut/py-googletrans)*

## Basic Procedures
-  Basic Use
> 1. Launch the application.
> 2. Choose a program.
> 3. Screenshot the chosen program.  **-> All outputs will be released on Text Widgets.**
- Jisho-API Use
> 1. Place any text(JP/EN) inside the Entry Widget.
> 2. Press Enter. **-> All outputs will be released on Label Widgets.**

## Notes
+ ***Currently screenshotting only works when the window is open, on top and not fullscreened.***
+ Temp Folder is responsible for holding screenshots of the current chosen window.
+ Image Folder is for miscellaneous files apart from Tesseract-OCR.

## Latest Release
* Version 0.1a [Pre-release]
  - _https://github.com/SaitoGH/vn-text-capture/releases/tag/0.1a_
