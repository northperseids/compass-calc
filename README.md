# compass-calc
Simple notepad calculator that allows in-line note-taking with simultaneous calculation.

![Image showing calculation window with various examples](/screenshots/image1.png)<br>
![Image showing constants window](/screenshots/image2.png)<br><br>

I'm still learning python - I wanted a calculator that I could simultaneously take notes in, and I couldn't find one that really suited my needs, and I figured it would be a good learning project, so I made one.

Currently it can handle most basic arithmetic, but it's still got a lot of room to improve.

Current supported conversions:
- inch -> mm, cm, ft, yards
- mm -> inches, cm, ft
- cm -> inches, mm, ft
- feet -> inches, mm, cm
- meter -> inches, mm, ft, cm

This is still a work in progress.

### Future plans/current issues
- ~~Change eval() to an actual parser~~ - DONE, simple math parser added, still being updated
  - ~~Make it able to handle negative numbers more easily in expressions~~ DONE
- Fix that it won't automatically multiply something next to parentheses (i.e. 2(4) will not come out as 2*4=8)
- Expand on conversions
- ~~Add basic trig functions~~ DONE, can handle sin, cos, tan, and so far can handle nested trig functions as well (sin(cos(2)) for example)
