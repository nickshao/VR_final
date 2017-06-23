from PIL import Image
import sys
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--origin',type=str)
parser.add_argument('--after', type=str)
parser.add_argument('--radius', type=int)
parser.add_argument('--intensity', type=int)
args = parser.parse_args()
def read_img(file_path):
    origin = Image.open(file_path)
    width, height = origin.size
    return origin, width, height
def oil_painting(origin, radius, Intensity, width, height):
    final_img = Image.new("RGB", (width, height), "white")
    print('pixel:',origin.getpixel((0,0)))
    print('width, height:', width,height)
    for nX in range(radius, width - radius):
        for nY in range(radius, height - radius):
            print('nX, nY: ',nX, nY)
            nSumR = np.zeros((256, ), dtype=np.int)
            nSumG = np.zeros((256, ), dtype=np.int)
            nSumB = np.zeros((256, ), dtype=np.int)
            nIntensityCount = np.zeros((256, ), dtype=np.int)
            for nX_O in range((-1)*radius, radius+1):
                for nY_O in range((-1)*radius, radius+1):
                    nR = origin.getpixel((nX + nX_O, nY + nY_O))[0]
                    nG = origin.getpixel((nX + nX_O, nY + nY_O))[1]
                    nB = origin.getpixel((nX + nX_O, nY + nY_O))[2]
                    CurIntensity = min(int((((nR+nG+nB)/3.)*Intensity)//255),255)
                    i = CurIntensity
                    nIntensityCount[i] += 1
                    nSumR[i] += nR
                    nSumG[i] += nG
                    nSumB[i] += nB
            nMaxIndex = np.argmax(nIntensityCount)
            nCurMax = nIntensityCount[nMaxIndex]
            final_color = []
            final_color.append(int(nSumR[nMaxIndex] // nCurMax))
            final_color.append(int(nSumG[nMaxIndex] // nCurMax))
            final_color.append(int(nSumB[nMaxIndex] // nCurMax))
            final_img.putpixel((nX, nY), tuple(final_color))
    final_img.save(args.after)
if __name__ == '__main__':
    origin, width, height = read_img(args.origin)
    oil_painting(origin, args.radius, args.intensity, width, height)

