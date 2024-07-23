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


def custom_order(filename):
    # Define the custom order of Total, {RE: "Er", "Ce", "Eu", "Ho", "Pr", "Sm", "Dy", "Gd", "La", "Nd", "Tb", "Lu"}, Fe, and Si
    order = {
        "Total": 0,
        "Int": 1,
        "Er": 1,
        "Ce": 1,
        "Eu": 1,
        "Ho": 1,
        "Pr": 1,
        "Sm": 1,
        "Dy": 1,
        "Gd": 1,
        "La": 1,
        "Nd": 1,
        "Tb": 1,
        "Lu": 1,
        "Fe": 2,
        "Si": 3,
    }
    # Return the corresponding order value
    return order.get(label, 999)