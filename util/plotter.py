import click
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import ticker
import re
from collections import defaultdict
from util.getter import (
    get_cohp_files,
    get_coop_files,
    get_dos_files,
    custom_order,
)
from util.classifier import classify_element, element_colors, additional_colors

# Global variable to store subtraction values
subtraction_values = {}

color_map = {}
colors = ["red", "green", "blue", "orange", "teal"]
color_index = 0


def plot_cohp_contributions(directory):
    cohp_files = get_cohp_files(directory)

    # Close all existing figures to avoid displaying multiple figures
    plt.close("all")

    # Adjust figure size for display (smaller figsize)
    fig, ax = plt.subplots(figsize=(5.4, 12))  # smaller figsize for display

    all_x_values = []

    # Group COHP files by parent folder
    cohp_groups = defaultdict(list)
    for filename in cohp_files:
        parent_folder = os.path.basename(os.path.dirname(filename))
        cohp_groups[parent_folder].append(filename)

    handles = []  # List to store legend handles
    labels = []  # List to store legend labels

    global color_index  # Use global color_index to keep track of color usage

    for parent_folder, filenames in cohp_groups.items():
        for filename in filenames:
            # Read data from file
            data = np.loadtxt(filename)

            # Check if file starts with "Int" and multiply y-values by -1
            if os.path.basename(filename).startswith("COHP-Int"):
                data[:, 1] *= -1
                linestyle = "--"  # Dashed line for 'Int' files
            else:
                linestyle = "-"  # Solid line for non-'Int' files

            # Subtract corresponding value from y-values
            y = data[:, 1]
            if parent_folder in subtraction_values:
                y -= subtraction_values[parent_folder]

            # Collect x-values within the specified y-axis range for dynamic x-axis limits
            x = data[:, 0]
            valid_indices = (y >= -6) & (y <= 3)
            all_x_values.extend(x[valid_indices])

            # Plot the data on the same axis with default colors
            file_name = os.path.splitext(os.path.basename(filename))[0]
            pair_name = file_name.replace("COHP-", "").replace(
                "Int ", ""
            )  # Extract pair name

            if pair_name not in color_map:
                color_map[pair_name] = colors[color_index % len(colors)]
                color_index += 1
            color = color_map[pair_name]

            (line,) = ax.plot(
                x,
                y,
                label=file_name.replace("COHP-", ""),
                linestyle=linestyle,
                linewidth=2.5,
                color=color,
            )
            handles.append(line)  # Append handle to list
            labels.append(
                file_name.replace("COHP-", "")
            )  # Append label to list

    # Determine the maximum absolute x-value within the y-limits
    max_x = max(abs(min(all_x_values)), abs(max(all_x_values)))

    # Plot a line at y=0 and x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=2.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=2.5)

    # Remove x-axis ticks and labels for both axes
    ax.xaxis.set_visible(False)

    # Set font size for ticks
    ax.tick_params(
        axis="y", labelsize=25, direction="in", width=2.5, length=14
    )  # Set y-axis ticks inside with width=2.5

    # Custom formatter to ensure proper minus sign rendering
    formatter = ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel("Energy (eV)", fontsize=28)  # Set font size for y-axis label
    ax.set_title(
        "", fontsize=35, pad=5
    )  # Set an empty title to remove file name
    ax.set_xlim(-max_x * 1.2, max_x * 1.2)  # Set the x-axis limits dynamically
    ax.set_ylim(-6, 3)  # Set the y-axis limits
    ax.yaxis.set_major_locator(
        MaxNLocator(integer=True)
    )  # Show only whole numbers on y-axis

    # Sort labels and handles
    sorted_labels_handles = sorted(zip(labels, handles), key=lambda x: x[0])

    # Unzip the sorted labels and handles
    sorted_labels, sorted_handles = zip(*sorted_labels_handles)

    # Filter out labels and handles that start with "Int"
    filtered_labels_handles = [
        (label, handle)
        for label, handle in zip(sorted_labels, sorted_handles)
        if not label.startswith("Int")
    ]

    # Unzip the filtered labels and handles
    filtered_labels, filtered_handles = zip(*filtered_labels_handles)

    # Add legend to the plot with Int dashed
    legend = ax.legend(
        filtered_handles,
        filtered_labels,
        frameon=False,
        fontsize=23,
        handlelength=1.0,
    )  # Remove legend frame
    for line, label in zip(legend.get_lines(), legend.get_texts()):
        line.set_linewidth(2.5)
        if "Int" in label.get_text():  # Check if the label contains 'Int'
            line.set_linestyle("--")  # Set linestyle to dashed

    # Add common title on the top
    folder_name = os.path.basename(directory)
    folder_name_subscripted = re.sub(
        r"(\d+)", lambda x: r"$_\mathrm{" + x.group(0) + r"}$", folder_name
    )
    plt.suptitle(
        folder_name_subscripted + " COHP",
        fontsize=30,
        y=1.0,
        ha="right",
        x=0.82,
    )

    # Calculate annotation position based on current data limits
    y_min, y_max = ax.get_ylim()
    annotation_y = 0  # Place annotation exactly at y=0
    annotation_x = max_x * 1.2  # Adjust x position dynamically

    # Add E_F annotation outside the plot to the right
    ax.annotate(
        r"$E_{\mathrm{F}}$",
        xy=(annotation_x, annotation_y),
        xytext=(10, 0),
        xycoords="data",
        textcoords="offset points",
        fontsize=25,
        va="center",
        ha="left",
        color="black",
    )

    # Prompt for adding an adjusted Fermi level line
    add_adj_fermi_level = click.prompt(
        "Would you like to add a horizontal line signifying the adjusted Fermi level? (y/n)",
        type=str,
    )
    click.echo("Please close the plot window to proceed")
    if add_adj_fermi_level.lower() == "y":
        adj_fermi_level_y = click.prompt(
            "Enter the y-value for the adjusted Fermi level line:", type=float
        )
        ax.axhline(
            adj_fermi_level_y, color="black", linestyle="-.", linewidth=2.5
        )
        ax.annotate(
            r"Adj. $E_{\mathrm{F}}$",
            xy=(annotation_x, adj_fermi_level_y),
            xytext=(10, 0),
            xycoords="data",
            textcoords="offset points",
            fontsize=25,
            va="center",
            ha="left",
            color="black",
        )

    # Adjust the layout manually
    plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1)

    ax.spines["top"].set_linewidth(2.5)
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)

    # Display the plot
    plt.show()

    # Prompt user for feedback on y-axis limits
    while True:
        feedback = click.prompt(
            "Are the displayed y-axes appropriate? (y/n)", type=str
        )
        if feedback.lower() == "y":
            break
        elif feedback.lower() == "n":
            y_min_new = click.prompt("Enter the new y-min:", type=float)
            y_max_new = click.prompt("Enter the new y-max:", type=float)
            if y_min_new == y_max_new:
                click.echo(
                    "Entered max and min are the same. Please correct it."
                )
            else:
                ax.set_ylim(y_min_new, y_max_new)
                plt.show()
                break
        else:
            click.echo("Invalid input. Please enter 'y' or 'n'.")

    # Save the plot as PNG in the grandparent folder of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(script_dir)
    output_filename = os.path.join(grandparent_dir, folder_name + "_COHP.png")
    fig.savefig(output_filename, bbox_inches="tight")


def plot_coop_contributions(directory):
    coop_files = get_coop_files(directory)

    # Close all existing figures to avoid displaying multiple figures
    plt.close("all")

    # Adjust figure size for display (smaller figsize)
    fig, ax = plt.subplots(figsize=(5.4, 12))  # smaller figsize for display

    all_x_values = []

    # Group COOP files by parent folder
    coop_groups = defaultdict(list)
    for filename in coop_files:
        parent_folder = os.path.basename(os.path.dirname(filename))
        coop_groups[parent_folder].append(filename)

    handles = []  # List to store legend handles
    labels = []  # List to store legend labels

    global color_index  # Use global color_index to keep track of color usage

    for parent_folder, filenames in coop_groups.items():
        for filename in filenames:
            # Read data from file
            data = np.loadtxt(filename)

            # Check if file starts with "Int" and multiply y-values by -1
            if os.path.basename(filename).startswith("COOP-Int"):
                data[:, 1] *= -1
                linestyle = "--"  # Dashed line for 'Int' files
            else:
                linestyle = "-"  # Solid line for non-'Int' files

            # Subtract corresponding value from y-values
            y = data[:, 1]
            if parent_folder in subtraction_values:
                y -= subtraction_values[parent_folder]

            # Collect x-values within the specified y-axis range for dynamic x-axis limits
            x = data[:, 0]
            valid_indices = (y >= -6) & (y <= 3)
            all_x_values.extend(x[valid_indices])

            # Plot the data on the same axis with default colors
            file_name = os.path.splitext(os.path.basename(filename))[0]
            pair_name = file_name.replace("COOP-", "").replace(
                "Int ", ""
            )  # Extract pair name

            if pair_name not in color_map:
                color_map[pair_name] = colors[color_index % len(colors)]
                color_index += 1
            color = color_map[pair_name]

            (line,) = ax.plot(
                x,
                y,
                label=file_name.replace("COOP-", ""),
                linestyle=linestyle,
                linewidth=2.5,
                color=color,
            )
            handles.append(line)  # Append handle to list
            labels.append(
                file_name.replace("COOP-", "")
            )  # Append label to list

    # Determine the maximum absolute x-value within the y-limits
    max_x = max(abs(min(all_x_values)), abs(max(all_x_values)))

    # Plot a line at y=0 and x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=2.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=2.5)

    # Remove x-axis ticks and labels for both axes
    ax.xaxis.set_visible(False)

    # Set font size for ticks
    ax.tick_params(
        axis="y", labelsize=25, direction="in", width=2.5, length=14
    )  # Set y-axis ticks inside with width=2.5

    # Custom formatter to ensure proper minus sign rendering
    formatter = ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel("Energy (eV)", fontsize=28)  # Set font size for y-axis label
    ax.set_title(
        "", fontsize=35, pad=5
    )  # Set an empty title to remove file name
    ax.set_xlim(-max_x * 1.2, max_x * 1.2)  # Set the x-axis limits dynamically
    ax.set_ylim(-6, 3)  # Set the y-axis limits
    ax.yaxis.set_major_locator(
        MaxNLocator(integer=True)
    )  # Show only whole numbers on y-axis

    # Sort labels and handles
    sorted_labels_handles = sorted(zip(labels, handles), key=lambda x: x[0])

    # Unzip the sorted labels and handles
    sorted_labels, sorted_handles = zip(*sorted_labels_handles)

    # Filter out labels and handles that start with "Int"
    filtered_labels_handles = [
        (label, handle)
        for label, handle in zip(sorted_labels, sorted_handles)
        if not label.startswith("Int")
    ]

    # Unzip the filtered labels and handles
    filtered_labels, filtered_handles = zip(*filtered_labels_handles)

    # Add legend to the plot with Int dashed
    legend = ax.legend(
        filtered_handles,
        filtered_labels,
        frameon=False,
        fontsize=23,
        handlelength=1.0,
    )  # Remove legend frame
    for line, label in zip(legend.get_lines(), legend.get_texts()):
        line.set_linewidth(2.5)
        if "Int" in label.get_text():  # Check if the label contains 'Int'
            line.set_linestyle("--")  # Set linestyle to dashed

    # Add common title on the top
    folder_name = os.path.basename(directory)
    folder_name_subscripted = re.sub(
        r"(\d+)", lambda x: r"$_\mathrm{" + x.group(0) + r"}$", folder_name
    )
    plt.suptitle(
        folder_name_subscripted + " COOP",
        fontsize=30,
        y=1.0,
        ha="right",
        x=0.82,
    )

    # Calculate annotation position based on current data limits
    y_min, y_max = ax.get_ylim()
    annotation_y = 0  # Place annotation exactly at y=0
    annotation_x = max_x * 1.2  # Adjust x position dynamically

    # Add E_F annotation outside the plot to the right
    ax.annotate(
        r"$E_{\mathrm{F}}$",
        xy=(annotation_x, annotation_y),
        xytext=(10, 0),
        xycoords="data",
        textcoords="offset points",
        fontsize=25,
        va="center",
        ha="left",
        color="black",
    )

    # Prompt for adding an adjusted Fermi level line
    add_adj_fermi_level = click.prompt(
        "Would you like to add a horizontal line signifying the adjusted Fermi level? (y/n)",
        type=str,
    )
    click.echo("Please close the plot window to proceed")
    if add_adj_fermi_level.lower() == "y":
        adj_fermi_level_y = click.prompt(
            "Enter the y-value for the adjusted Fermi level line:", type=float
        )
        ax.axhline(
            adj_fermi_level_y, color="black", linestyle="-.", linewidth=2.5
        )
        ax.annotate(
            r"Adj. $E_{\mathrm{F}}$",
            xy=(annotation_x, adj_fermi_level_y),
            xytext=(10, 0),
            xycoords="data",
            textcoords="offset points",
            fontsize=25,
            va="center",
            ha="left",
            color="black",
        )

    # Adjust the layout manually
    plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1)

    ax.spines["top"].set_linewidth(2.5)
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)

    # Display the plot
    plt.show()

    # Prompt user for feedback on y-axis limits
    while True:
        feedback = click.prompt(
            "Are the displayed y-axes appropriate? (y/n)", type=str
        )
        if feedback.lower() == "y":
            break
        elif feedback.lower() == "n":
            y_min_new = click.prompt("Enter the new y-min:", type=float)
            y_max_new = click.prompt("Enter the new y-max:", type=float)
            if y_min_new == y_max_new:
                click.echo(
                    "Entered max and min are the same. Please correct it."
                )
            else:
                ax.set_ylim(y_min_new, y_max_new)
                plt.show()
                break
        else:
            click.echo("Invalid input. Please enter 'y' or 'n'.")

    # Save the plot as PNG in the grandparent folder of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(script_dir)
    output_filename = os.path.join(grandparent_dir, folder_name + "_COOP.png")
    fig.savefig(output_filename, bbox_inches="tight")


def plot_dos_contributions(directory):
    dos_files = get_dos_files(directory)

    plt.close("all")

    fig, ax = plt.subplots(figsize=(5.4, 12))
    plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1)

    all_x_values = []
    y_min = -8
    y_max = 2

    # Initialize dictionaries for tracking occurrences
    group_elements = {}
    elements_by_group = {}
    total_plot = None

    for filename in dos_files:
        data = np.loadtxt(filename)
        x = data[:, 0]
        y = data[:, 1]
        file_name = os.path.splitext(os.path.basename(filename))[0]

        parent_folder = os.path.basename(directory)
        if parent_folder in subtraction_values:
            y -= subtraction_values[parent_folder]

        valid_indices = (y >= y_min) & (y <= y_max)
        all_x_values.extend(x[valid_indices])

        label = re.sub(r'(?i)dos-', '', file_name)  # Remove prefix from label

        if "Int" in label:
            continue

        element = label
        group = classify_element(element)

        # Track elements within their groups
        if group not in group_elements:
            group_elements[group] = []
        group_elements[group].append(element)

        if group not in elements_by_group:
            elements_by_group[group] = []
        color = element_colors.get(group, "gray")

        linestyle = "-"  # Default linestyle
        if element == "Total":
            color = "black"  # Ensure Total is black
            linestyle = "-"  # Solid line for Total

        elements_by_group[group].append((element, x, y, color, linestyle))

    # Apply color based on occurrence within each group
    for group, elements in group_elements.items():
        sorted_elements = sorted(elements)  # Sort alphabetically
        color_mapping = {elem: element_colors.get(group, "gray") for elem in sorted_elements}
        
        if len(sorted_elements) > 1:
            color_mapping[sorted_elements[1]] = additional_colors[0]  # Use additional color for second occurrence
        if len(sorted_elements) > 2:
            color_mapping[sorted_elements[2]] = additional_colors[1]  # Use another additional color for third occurrence

        # Update the color for each element in the group
        for i, (element, x, y, _, linestyle) in enumerate(elements_by_group[group]):
            elements_by_group[group][i] = (element, x, y, color_mapping[element], linestyle)

    # Plot Total first
    for group in elements_by_group:
        for element, x, y, color, linestyle in elements_by_group[group]:
            if element == "Total":
                total_plot = (x, y, element, color)
                break
        if total_plot:
            break

    sorted_elements = []

    # Plot Total line first
    if total_plot:
        x, y, label, color = total_plot
        (total_line,) = ax.plot(x, y, label=label, color="black", linestyle='-', linewidth=2.5)
        sorted_elements.append((total_line, label))

    # Sort by group order and then alphabetically within each group
    for group in sorted(elements_by_group, key=lambda g: custom_order(g)):
        elements = sorted(elements_by_group[group], key=lambda x: x[0])  # Sort alphabetically
        for element, x, y, color, linestyle in elements:
            if element != "Total":
                (line,) = ax.plot(x, y, label=element, color=color, linestyle=linestyle, linewidth=2.5)
                sorted_elements.append((line, element))

    # Separate sorted lines and labels
    sorted_plots, sorted_labels = zip(*sorted_elements)

    # Add legend to the plot based on sorted order
    legend = ax.legend(
        handles=sorted_plots,
        labels=sorted_labels,
        frameon=False,
        fontsize=23,
        handlelength=1.0,
    )
    for line in legend.get_lines():
        line.set_linewidth(2.5)

    # Continue with the rest of the plotting setup
    max_x_value_within_y_frame = max(all_x_values, key=abs) if all_x_values else 0
    ax.axhline(0, color="black", linestyle="--", linewidth=2.5)
    ax.xaxis.set_visible(False)
    ax.tick_params(
        axis="y", labelsize=25, direction="in", width=2.5, length=14, right=True
    )
    formatter = ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel("DOS", fontsize=28)
    ax.set_ylabel("Energy (eV)", fontsize=28)
    folder_name = os.path.basename(directory)
    folder_name_subscripted = re.sub(
        r"(\d+)", lambda x: r"$_\mathrm{" + x.group(0) + r"}$", folder_name
    )
    ax.set_title(folder_name_subscripted + " DOS", fontsize=30, pad=5, y=1.02)

    ax.set_xlim(0, max_x_value_within_y_frame * 1.2)
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    annotation_x = max_x_value_within_y_frame * 1.2
    ax.annotate(
        r"$E_{\mathrm{F}}$",
        xy=(annotation_x, 0),
        xytext=(10, 0),
        xycoords="data",
        textcoords="offset points",
        fontsize=25,
        va="center",
        ha="left",
        color="black",
    )

    plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1)
    ax.spines["top"].set_linewidth(2.5)
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)

    click.echo("Please close the plot window to proceed")

    plt.show()

    while True:
        feedback = click.prompt(
            "Are the displayed y-axes appropriate? (y/n)", type=str
        )
        if feedback.lower() == "y":
            break
        elif feedback.lower() == "n":
            y_min_new = click.prompt("Enter the new y-min:", type=float)
            y_max_new = click.prompt("Enter the new y-max:", type=float)
            if y_min_new == y_max_new:
                click.echo(
                    "Entered max and min are the same. Please correct it."
                )
            else:
                ax.set_ylim(y_min_new, y_max_new)
                plt.show()
                break
        else:
            click.echo("Invalid input. Please enter 'y' or 'n'.")

    add_adj_fermi_level = click.prompt(
        "Would you like to add a horizontal line signifying the adjusted Fermi level? (y/n)",
        type=str,
    )
    if add_adj_fermi_level.lower() == "y":
        adj_fermi_level_y = click.prompt(
            "Enter the y-value for the adjusted Fermi level line:", type=float
        )
        ax.axhline(
            adj_fermi_level_y, color="black", linestyle="-.", linewidth=2.5
        )
        ax.annotate(
            r"Adj. $E_{\mathrm{F}}$",
            xy=(annotation_x, adj_fermi_level_y),
            xytext=(10, 0),
            xycoords="data",
            textcoords="offset points",
            fontsize=25,
            va="center",
            ha="left",
            color="black",
        )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(script_dir)
    output_filename = os.path.join(grandparent_dir, folder_name + "_DOS.png")
    fig.savefig(output_filename, bbox_inches="tight")


def plot_dos_int_contributions(directory):
    dos_files = get_dos_files(directory)
    fig, ax = plt.subplots(figsize=(7, 14))  # Adjusted figure size
    ax_int = ax.twiny()  # Secondary x-axis for Dos-Int scale

    plt.subplots_adjust(left=0.22, top=0.84, right=0.8)  # Increase margins

    # Initialize lists to store handles and labels for legend
    handles = []
    labels = []

    y_min, y_max = -8, 2  # Default y-axis limits

    max_x_value_total_within_yframe = (
        -np.inf
    )  # Initialize max x-value for Total within y-frame
    max_x_value_int_within_yframe = (
        -np.inf
    )  # Initialize max x-value for Int within y-frame

    for filename in dos_files:
        # Check if filename contains '+'
        if "Dos-Total" not in filename and "Dos-Int" not in filename:
            continue  # Only plot total and int

        # Read data from file
        data = np.loadtxt(filename)

        # Split x and y values
        x = data[:, 0]
        y = data[:, 1]

        # Get file name without extension
        file_name = os.path.splitext(os.path.basename(filename))[0]

        # Get parent folder label
        parent_folder = os.path.basename(directory)

        # Multiply "Int" values by -1 - due to formatting of integration from wxDragon
        if "Int" in file_name:
            y *= -1

        # Subtract corresponding value from y-values
        if parent_folder in subtraction_values:
            y -= subtraction_values[parent_folder]

        # Plot the data
        label = file_name.replace(
            "Dos-", ""
        )  # Remove 'Dos-' prefix from label

        # Assign colors and line styles based on element
        color = "blue"  # Default color for most elements
        line_style = "-"  # Default line style
        if "Total" in label:
            color = "black"  # Total DOS in black
            line_style = "-"
            # Filter x-values based on y-frame
            x_filtered = x[(y >= y_min) & (y <= y_max)]
            if x_filtered.size > 0:
                max_x_value_total_within_yframe = max(
                    max_x_value_total_within_yframe, max(x_filtered)
                )
        elif "Int" in label:
            label = "Int"  # Change label to 'Int'
            color = "orange"
            line_style = "--"  # Dashed line for "Int" DOS
            # Filter x-values based on y-frame
            x_filtered = x[(y >= y_min) & (y <= y_max)]
            if x_filtered.size > 0:
                max_x_value_int_within_yframe = max(
                    max_x_value_int_within_yframe, max(x_filtered)
                )

        # Plot the data
        if "Int" in file_name:
            (line,) = ax_int.plot(
                x, y, label=label, color=color, linestyle=line_style
            )  # Store the handle
        else:
            (line,) = ax.plot(
                x, y, label=label, color=color, linestyle=line_style
            )  # Store the handle

        handles.append(line)  # Append handle to list
        labels.append(label)  # Append label to list

    (line,) = ax.plot(x, y, label=label, color=color, linewidth=2.5)

    # Set x-axis limits for both axes
    ax.set_xlim(-1, max_x_value_total_within_yframe * 1.25)
    ax_int.set_xlim(-1, max_x_value_int_within_yframe * 1)

    # Use regular expression to find numbers and subscript them
    folder_name = os.path.basename(directory)
    folder_name_subscripted = re.sub(
        r"(\d+)", lambda x: r"$_\mathrm{" + x.group(0) + r"}$", folder_name
    )
    folder_name_subscripted = folder_name_subscripted.replace(
        "DOS", "Dos"
    )  # Replace "DOS" with "Dos"

    ax.set_xlabel("DOS", fontsize=35)  # Set font size for x-axis label
    ax.set_ylabel("Energy (eV)", fontsize=28)  # Set font size for y-axis

    ax.set_title(
        folder_name_subscripted + " DOS", fontsize=35, pad=20
    )  # Set font size for title and add padding

    ax.set_ylim(-8, 2)  # Set the y-axis limits for specific parent folders

    ax.xaxis.set_major_locator(
        MaxNLocator(integer=True, nbins=5)
    )  # Show only 6 whole numbers on x-axis
    ax.axhline(
        0, color="black", linestyle="--", linewidth=2.5
    )  # Set line width to 3.2 for dashed line
    ax.text(
        ax.get_xlim()[1] + 0.02 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
        0,
        r"$E_{\mathrm{F}}$",
        fontsize=30,
        va="center",
        ha="left",
        color="black",
    )  # Set font size for annotation text and italicize 'E'

    # Apply custom formatter to y-axis
    formatter = ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    ax.yaxis.set_major_formatter(formatter)

    # Set font size for legend and sort labels based on custom order
    sorted_handles, sorted_labels = zip(
        *sorted(zip(handles, labels), key=lambda x: custom_order(x[1]))
    )
    legend = ax.legend(
        sorted_handles,
        sorted_labels,
        frameon=False,
        fontsize=25,
        handlelength=1.0,
    )  # Remove legend frame
    for text in legend.get_texts():
        text.set_fontsize(25)
    for line in legend.get_lines():
        line.set_linewidth(2.5)

    # Customize y-axis tick marks
    ax.tick_params(
        axis="y",
        direction="in",
        length=16,
        width=2.5,
        colors="black",
        which="both",
        labelsize=35,
    )  # Set font size for tick labels and thicker ticks

    # Customize x-axis tick marks and labels
    ax.tick_params(
        axis="x",
        which="both",
        bottom=True,
        top=False,
        labelbottom=True,
        labelsize=35,
        length=16,
        width=2.5,
    )  # Set font size for tick labels and adjust width

    # Set axes lines width to 2.5
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)

    # Duplicate y-axis limits and ticks for the secondary x-axis
    ax_int.set_xlim(ax.get_xlim())
    ax_int.set_xticks(
        np.linspace(0, max_x_value_int_within_yframe, 5)
    )  # Set ticks based on interval
    ax_int.set_xticklabels(
        [
            f"{int(i)}"
            for i in np.linspace(0, max_x_value_int_within_yframe, 5)
        ],
        fontsize=35,
    )  # Set font size for top x-axis tick labels

    # Set axes lines width to 2.5 for the secondary x-axis
    for spine in ax_int.spines.values():
        spine.set_linewidth(2.5)

    ax_int.set_xlabel(
        "IDOS", fontsize=35, labelpad=20
    )  # Set x-axis label for secondary x-axis
    ax_int.tick_params(width=2.5, which="both", length=16)

    click.echo("Please close the plot window to proceed")

    plt.show()

    # Prompt user for feedback on y-axis limits
    while True:
        feedback = click.prompt(
            "Are the displayed y-axes appropriate? (y/n)", type=str
        )
        if feedback.lower() == "y":
            break
        elif feedback.lower() == "n":
            y_min_new = click.prompt("Enter the new y-min:", type=float)
            y_max_new = click.prompt("Enter the new y-max:", type=float)
            if y_min_new == y_max_new:
                click.echo(
                    "Entered max and min are the same. Please correct it."
                )
            else:
                ax.set_ylim(y_min_new, y_max_new)
                plt.show()
                break
        else:
            click.echo("Invalid input. Please enter 'y' or 'n'.")

    # Prompt for adding an adjusted Fermi level line
    add_adj_fermi_level = click.prompt(
        "Would you like to add a horizontal line signifying the adjusted Fermi level? (y/n)",
        type=str,
    )
    if add_adj_fermi_level.lower() == "y":
        adj_fermi_level_y = click.prompt(
            "Enter the y-value for the adjusted Fermi level line:", type=float
        )
        ax.axhline(
            adj_fermi_level_y, color="black", linestyle="-.", linewidth=2.5
        )
        ax.annotate(
            r"Adj. $E_{\mathrm{F}}$",
            xy=(ax.get_xlim()[1], adj_fermi_level_y),
            xytext=(10, 0),
            xycoords="data",
            textcoords="offset points",
            fontsize=25,
            va="center",
            ha="left",
            color="black",
        )

    # Save the plot as PNG in the grandparent folder of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(script_dir)
    output_filename = os.path.join(
        grandparent_dir, folder_name + "_Int_DOS.png"
    )
    fig.savefig(output_filename, bbox_inches="tight")