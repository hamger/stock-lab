import tushare as ts
import pandas as pd
from lab import Lab
import option


def main():
    args = option.parser.parse_args()
    print('Lab is starting...\n')
    stockh = Lab(args)
    stockh.run()
    print('\nLab is done...')


if __name__ == '__main__':
    main()
