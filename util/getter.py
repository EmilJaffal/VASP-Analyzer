import os
import glob
import click


def get_cohp_files(directory):
    # Use glob to find all files starting with "COHP-", "cohp-", or "Cohp-" in the specified directory
    cohp_files = glob.glob(os.path.join(directory, "[Cc][Oo][Hh][Pp]-*"))
    if not cohp_files:
        click.echo("COHP/COOP files not found.")
    return cohp_files


def get_coop_files(directory):
    # Use glob to find all files starting with "COOP-", "coop-", or "Coop-" in the specified directory
    coop_files = glob.glob(os.path.join(directory, "[Cc][Oo][Oo][Pp]-*"))
    if not coop_files:
        click.echo("COOP files not found.")
    return coop_files


def get_dos_files(directory):
    # Use glob to find all files starting with "DOS-", "dos-", or "Dos-" in the specified directory
    dos_files = glob.glob(os.path.join(directory, "[Dd][Oo][Ss]-*"))
    if not dos_files:
        click.echo("DOS files not found.")
    return dos_files

def get_doe_files(directory):
    # Use glob to find all files starting with "DOS-", "dos-", or "Dos-" in the specified directory
    doe_files = glob.glob(os.path.join(directory, "[Dd][Oo][Ee]-*"))
    if not doe_files:
        click.echo("DOE file not found.")
    return doe_files


def custom_order(label):
    # Define the custom order of Total, Transition Metals, Alkali Metals, Alkaline Earth Metals, Lanthanides,
    # Actinides, Metalloids, Halogens, Noble Gases, Post-transition Metals, and Other
    order = {
        "Total": 0,
        "Transition Metals": 1,
        "Alkali Metals": 2,
        "Alkaline Earth Metals": 3,
        "Lanthanides": 4,
        "Actinides": 5,
        "Metalloids": 6,
        "Halogens": 7,
        "Noble Gases": 8,
        "Post-transition Metals": 9,
        "Other": 10,
    }
    # Return the corresponding order value
    return order.get(label, 999)