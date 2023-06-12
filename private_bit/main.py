import os
import argparse
from lxml import etree


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入MP3音频 (音频同目录需要有010editor导出的Xml文件!)')
parser.add_argument("-hex", nargs='?', const=True, default=False,
                    help="使用hex编码输出")
parser.add_argument("-v", nargs='?', const=True, default=False,
                    help="使用hex编码输出")
args  = parser.parse_args()

if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    baseDir = os.path.dirname(filePath)
    fileSuffix, ext = os.path.splitext(filePath)
    fileName = fileSuffix.split("\\")[-1]

    xmlPath = os.path.join(baseDir, f"{fileName}.xml")
    if not os.path.exists(xmlPath):
        print("没有找到010editor导出的xml文件!")
        exit(-1)

    with open(xmlPath, "rb") as f:
        root = etree.HTML(f.read())
    starts = root.xpath("//variable[starts-with(name, 'struct MPEG_FRAME mf')]/start/text()")

    bin_str = ""
    with open(filePath, "rb") as f:
        for start in starts:
            f.seek(int(str(start)[:-1], 16), 0)
            bin_str += f"{f.read(3)[-1] & 1}"

    if args.v:
        print(f"bits: {bin_str}")
    data = bytes((int(bin_str[i:i+8], 2)) for i in range(0, len(bin_str), 8))
    print(data.hex()) if args.hex else print(data)
    