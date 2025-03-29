# src/growclonego/main.py

import argparse
import pandas as pd
from .core import * # new_function

def main():
    parser = argparse.ArgumentParser(description="Process raw data file.")
    parser.add_argument('file_path', type=str, help="Path to the raw data file.")
    parser.add_argument('--pop0', type=float, help="Initial cell seeding count", required=False, default=float('nan'))
    parser.add_argument('--popf', type=float, help="Final cell count", required=False, default=float('nan'))
    parser.add_argument('--mean-pop-rate', type=float, help="Average growth rate of population (1/hr)", required=False)
    args = parser.parse_args()

    try:
        # Load data
        data = load_data(args.file_path) ## turn this into one funciton in core
        data = make_long(data)
        data = est_growth(data, pop0=args.pop0, popf=args.popf, mean_pop_rate=args.mean_pop_rate)
        print(data.head())
        data.to_csv("outs/growth_outs.csv", index=False)

        summary = summarize_growths(data)
        print(summary.head())
        summary.to_csv("outs/summary_outs.csv", index=False)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
