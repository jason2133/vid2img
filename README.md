# vid2img
Extract frames from a video. Keep it simple stupid.

# Extentions
- Worked
	+ mp4, 3gp, avi, flv, m4v, mov, mpeg, vob, mpg, mts, wmv
- NOT Worked
	+ webm, mkvm

# Requirements
```
pip install -r requirements.txt
```

# Usage
- usage
```
python vid2img.py [-h] [-o OUTDIR] [-i INTERVAL] [-e EXTENTION] [-p] path
```

- default
```
python vid2img.py path -o extracted -i 60 -e png
# Extracts :
# from the video file of "path"
# one frame per "60" frames,
# and save frames to "extracted"
# as "png" image.
```
