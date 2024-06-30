# VASP Analyzer
 
## Description

This is a tool to analyze various COOP, COHP and DOS files from VASP once imported to wxDragon as .xy files. wxDragon doesn't allow for a great amount of editing/visual stimulation when it comes to visualization, so the hope is that this can replace it as a better and simpler visualizer for those researchers who are not software-inclined. 

## How to Download

### Option 1: Using Git
Clone the repository: Open your terminal/command prompt and navigate to the directory where you want to store the project. 

Then, run the following command:

```bash
git clone https://github.com/EmilJaffal/VASP-Analyzer.git
```

Install the required libraries by running:

```bash
pip install -r requirements.txt
```

Navigate to the project directory by entering

```bash
cd VASP-Analyzer
```

and run with a folder of either COOP, COHP, and/or DOS files

```bash
python main.py
```

### Option 2: Download ZIP
- Download ZIP: Click the "Code" button on the repository page and select "Download ZIP".
- Extract the ZIP file: Once the download is complete, extract the ZIP file's contents to your desired location.

### How to Use

The software currently allows the user to plot COHP and COOP simultaneously, while maintaining the same color for element-pair contributions as it is common that both are plotted. If one or the other isn't found, it'll plot what's available without issue to the user. The DOS plotting gives the user the option to plot the total as well as elemental contributions (option 2) and to plot integrated total DOS with total DOS (option 3). The prompts also allow the user to add an adjusted Fermi level based on experimental occupancy data, as well as the Fermi level found in the DOSCAR files to shift the data.

To plot, simply put a folder named either something arbitrary or something specific such as the formula or structure type with the DOS/COHP/COOP files inside. These .xy files should be named COOP-[name], Coop-[name], or coop-[name] to be recognized up by the software. To indicate if it is spin-polarized, simply write it into the name.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For any questions, feedback, or issues, please open an issue on GitHub.