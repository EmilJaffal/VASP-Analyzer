import os
import click
from util.plotter import (
    plot_cohp_contributions,
    plot_coop_contributions,
    plot_dos_contributions,
    plot_dos_int_contributions,
    plot_doe_int_contributions,
    subtraction_values
)
from util.getter import get_cohp_files, get_coop_files, get_dos_files, get_doe_files


@click.command()
def analyze_folders():
    # Step 1: List folders in the directory where main.py is located
    root_dir = os.path.dirname(os.path.abspath(__file__))
    folders = [
        folder
        for folder in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, folder)) and folder not in {'util', '.git'}
    ]
    folders.sort()

    click.echo("Which of the following folders would you like to analyze?")
    for i, folder in enumerate(folders, start=1):
        click.echo(f"{i}. {folder}")

    choice = click.prompt(
        "Enter the number corresponding to the folder you want to analyze",
        type=int,
    )
    chosen_folder = folders[choice - 1]

    # Step 2: Prompt 'What files would you like to analyze?'
    click.echo("What files would you like to analyze?")
    click.echo("1. COOP/COHP files")
    click.echo("2. DOS files (elemental contributions)")
    click.echo("3. DOS files (total and integrated)")
    click.echo("4. Just COHP files")
    click.echo("5. DOE files (total and integrated)")


    file_choice = click.prompt(
        "Enter the number corresponding to the type of files you want to analyze",
        type=int,
    )

    directory = os.path.join(root_dir, chosen_folder)

    if file_choice == 1:
        # Check for COHP and COOP files
        cohp_files = get_cohp_files(directory)
        coop_files = get_coop_files(directory)
        if not cohp_files or not coop_files:
            click.echo("COHP/COOP files not found.")
            return  # Early return if no COHP/COOP files found

        # Prompt for Fermi level and calculate subtraction value
        fermi_level = click.prompt(
            "What is the Fermi level? (See line 6, third value of DOSCAR file)",
            type=float,
        )
        subtraction_values[chosen_folder] = fermi_level

        # Generate COHP and COOP plots for the chosen folder
        plot_cohp_contributions(directory)
        plot_coop_contributions(directory)

    elif file_choice == 2:
        # Check for DOS files
        dos_files = get_dos_files(directory)
        if not dos_files:
            click.echo("DOS files not found.")
            return  # Early return if no DOS files found

        # Prompt for Fermi level and calculate subtraction value
        fermi_level = click.prompt(
            "What is the Fermi level? (See line 6, third value of DOSCAR file)",
            type=float,
        )
        subtraction_values[chosen_folder] = fermi_level

        # Generate DOS plot for the chosen folder
        plot_dos_contributions(directory)

    elif file_choice == 3:
        # Check for DOS files
        dos_files = get_dos_files(directory)
        if not dos_files:
            click.echo("DOS files not found.")
            return  # Early return if no DOS files found

        # Prompt for Fermi level and calculate subtraction value
        fermi_level = click.prompt(
            "What is the Fermi level? (See line 6, third value of DOSCAR file)",
            type=float,
        )
        subtraction_values[chosen_folder] = fermi_level

        # Generate integrated DOS plot for the chosen folder
        plot_dos_int_contributions(directory)

    elif file_choice == 4:
        # Check for COHP files
        cohp_files = get_cohp_files(directory)
        if not cohp_files:
            click.echo("COHP files not found.")
            return  # Early return if no COHP files found

        # Prompt for Fermi level and calculate subtraction value
        fermi_level = click.prompt(
            "What is the Fermi level? (See line 6, third value of DOSCAR file)",
            type=float,
        )
        subtraction_values[chosen_folder] = fermi_level

        # Generate COHP plot for the chosen folder
        plot_cohp_contributions(directory)

    elif file_choice == 5:
        # Check for DOS files
        doe_files = get_doe_files(directory)
        if not doe_files:
            click.echo("DOE file not found.")
            return  # Early return if no DOS files found

        # Prompt for Fermi level and calculate subtraction value
        fermi_level = click.prompt(
            "What is the Fermi level? (See line 6, third value of DOSCAR file)",
            type=float,
        )
        subtraction_values[chosen_folder] = fermi_level

        # Generate integrated DOS plot for the chosen folder
        plot_doe_int_contributions(directory)

    else:
        click.echo("Invalid choice. Exiting.")


if __name__ == "__main__":
    analyze_folders()
