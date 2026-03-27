from pathlib import Path

def build_plot_markdown():
    report_path = Path('data_lake/silver/reports/plots.md')
    report_path.parent.mkdir(exist_ok=True)
        
    with open(report_path, 'w', encoding = 'utf-8') as f:
        f.write('# Data Visualization\n\n')

        f.write('## Fare Distribution\n')
        f.write('![fare](../plots/fare.png)\n\n')

        f.write('## Trip Distance\n')
        f.write('![distance](../plots/distance.png)\n\n')

        f.write('## Trips by Hour\n')
        f.write('![hour](../plots/hour.png)\n\n')

        f.write('## Distance vs Fare\n')
        f.write('![scatter](../plots/scatter.png)\n\n')

        f.write('## Top Pickup Locations\n')
        f.write('![zones](../plots/zones.png)\n\n')

build_plot_markdown()