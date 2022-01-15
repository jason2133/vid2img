import os
import argparse
from pathlib import Path
import cv2
from joblib import Parallel, delayed


class Vid2Img:

    def __init__(self, path, outdir, interval, ext):
        self.path = path
        self.outdir = outdir
        self.interval = interval
        self.ext = ext
        self.cores = os.cpu_count()
        self.make_outdir()
        self.read_vid()

    def make_outdir(self):
        if not self.outdir:
            self.outdir = Path("extracted")/self.path.stem
        if not self.outdir.exists():
            self.outdir.mkdir(exist_ok=True, parents=True)

    def read_vid(self):
        vid = cv2.VideoCapture(str(self.path))
        self.frame_cnt = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    def save_frames(self, parallel):
        if parallel:
            self.block = self.frame_cnt // (self.cores-1)
            self.positions = list(range(0, self.frame_cnt, self.block))
            proc = [delayed(self.save_block)(self.get_block(core)) for core in range(self.cores)]
            Parallel(n_jobs=self.cores, backend='threading', verbose=1)(proc)
        else:
            self.block = self.frame_cnt
            vid = cv2.VideoCapture(str(self.path))
            self.save_block(vid)

    def get_block(self, i):
        vid = cv2.VideoCapture(str(self.path))
        start = self.positions[i]
        vid.set(cv2.CAP_PROP_POS_FRAMES, start)
        return vid

    def save_block(self, vid):
        for idx in range(self.block):
            frame_cnt = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = vid.read()
            if frame_cnt % self.interval == 0 and ret:
                cv2.imwrite(f"{Path(self.outdir)/str(frame_cnt)}.{self.ext}", frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path,
                        help="Path to the input video.")
    parser.add_argument("-o", "--outdir", type=Path,
                        help="Directory to save the frames.")
    parser.add_argument("-i", "--interval", type=int, default=60,
                        help="Interval between the frames to save.")
    parser.add_argument("-e", "--extension", type=str, default="png",
                        help="Extension to save frames as.")
    parser.add_argument("-p", "--parallel", default=False, action='store_true',
                        help="Run the extraction in parallel.")
    args = parser.parse_args()

    vi = Vid2Img(args.path, args.outdir, args.interval, args.extension)
    vi.save_frames(args.parallel)
