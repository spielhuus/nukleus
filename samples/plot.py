import sys
import argparse

sys.path.append('src')
sys.path.append('../src')

import nukleus

def main():
    parser = argparse.ArgumentParser(description='plot a kicad schema file.')
    parser.add_argument('--input', dest='input', required=True,
                        help='the input filename.')
    parser.add_argument('--output', dest='output', required=True,
                        help='the output filename.')
    args = parser.parse_args()

    schema = nukleus.load_schema(args.input)
    nukleus.plot(schema, args.output, image_type='pdf')

#    with open(args.output, 'bw') as file:
#        file.write(image_bytes.getbuffer())

#display(SVG(data=bytes.getbuffer()))
#image = Image.open(bytes)
#image = Image.open(BytesIO(bytes.getbuffer()))


#image = Image.open('plot.svg')
#image.show()




if __name__ == "__main__":
    main()
