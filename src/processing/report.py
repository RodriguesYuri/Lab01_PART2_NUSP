from loader import load_data
from profiling import get_describe, get_info, get_nulls
from pathlib import Path

def build_report(data):
    report_path = Path('data_lake/silver/reports/report.md')
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w', encoding = 'utf-8') as f:
        f.write('# Report\n\n')

        for name, df in data.items():
            f.write(f'## Dataset: {name}\n\n')

            f.write('### Info\n')
            f.write(f'{get_info(df)}')
            f.write('\n\n')

            f.write('### Null Count\n')
            f.write(f'{get_nulls(df)}')
            f.write('\n\n')            

            f.write('### Describe\n')
            f.write(f'{get_describe(df)}')
            f.write('\n\n')

def main():
    data = load_data()
    build_report(data)

if __name__ == '__main__':
    main()