# ColorSeasonMatch

![](DemoVideo.mp4)

## Context
There are 12 different color seasons, and the theory is that only 1 looks best on each person. You can read more about color seasons [here](https://www.fineclothing.com/the-fine-line/color-analysis.html), but I also liked [this video](https://www.youtube.com/watch?v=X-VyDqCznnw&pp=ygUZY29sb3Igc2Vhc29uIHN0eWxlIHRoZW9yeQ%3D%3D) as an explanation as well.

This tool is meant to be used if you already know your color season.

## Finding Your Color Season
If you are in process of finding your color season, I strongly, strongly recommend against following the descriptions that websites will give (e.g. dark hair vs light hair is winter vs summer). The only way to get a proper color analysis done is by holding color swatches up to your face in the mirror. Take it from me, a brown skinned, black haired girl whose color season is light summer, do the color swatch test. Swatch appointments can often run 200+ dollars, but you can buy cloth samples for $30 on amazon, and with some manual sorting into seasons you can pretty easily find your color in a DIY at-home session with friends.

I also recommend downloading the My Best Colors app once you know your color for getting an idea of what colors look good on you.

## Why This Tool?
I made this because I was really struggling to tell different hues of colors apart. Is this pink more cool or warmed tone? And if I do answer that, what does that mean?
I'm a programmer, not a graphic designer, so colors are absolutely not my strong suit (if it wasn't obvious by the color scheme of this program LOL). So I needed this tool to tell me if the colors of the clothes I was looking to buy were really in my pallette or if I was stretching the definition of a light summer.

Some people will say "pinks look good on summers/springs" or generalized things like that, but I caution against saying that. Not all colors are the same, hence why we have seasons in the first place.

## Are Color Seasons Accurate?
I don't know. Part of me wonders if this is pseudo-intellectual stuff, especially when there's quizzes to find your color season the way that there are quizzes to find your MBTI type or love language. But I don't know enough about color theory to disprove it either. I do know that when I did a color swatch test with my friend, our respective color seasons stood out in such a way that neither of us imagined they would. (Like, 11/12 seasons made us look grey and only 1 looked good on each of us). So at least for myself, I found it to be adequately accurate.

I also found that I enjoy knowing my color season because it makes me feel more confident in my decisions when I buy clothes because that option of choice is taken away in a sense. 

## How does this tool work?
Baiscally, the image is taken and converted to RGB values, then we take the RGB value of the place you click and convert that to HSV which is said to be better for comparing colors. Then we take that HSV and find its closest matches within the color seasons.

Color season data was collected by taking screenshots from the My Best Colors app and running it through a similar algorithm (see ColorPickingToCsv.py). HSV, RGB, and Hex values of each season are saved in this project and can be used for free for any other projects.

## How To Run
`py ColorSeasonMatch.py`

## Dependencies
- Python
- CV2 (`pip install opencv-python`)
- Tk
- Colormath (`pip install colormath`)
- numpy

## Common problems
### 'numpy._DTypeMeta' object is not subscriptable
`pip install --upgrade numpy`

### module 'numpy' has no attribute 'asscalar'
Open the line where the error is coming from in color_diff.py

`Change numpy.asscalar(delta_e) to numpy.asarray(delta_e).item()`
This happens because asscalar was deprecated but the library we use, colormath, is no longer supported.

