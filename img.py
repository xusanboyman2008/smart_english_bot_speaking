import matplotlib.pyplot as plt
import numpy as np


def create_img_corrected(scores, name='Unknown'):
    # Criteria based on your uploaded image
    criteria = ['Accuracy', 'Fluency', 'Prosody', 'Grammar', 'Vocabulary', 'Topic']

    # Function to determine color based on score
    def get_color(score):
        if score >= 75:
            return 'green'
        elif score >= 50:
            return 'yellow'
        else:
            return 'red'

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot each criterion as a bar with its respective color and rounded edges
    bar_width = 0.6
    y_pos = np.arange(len(criteria))
    bars = ax.barh(y_pos, scores, color=[get_color(score) for score in scores], edgecolor='none', height=bar_width,
                   alpha=0.9, zorder=3, linewidth=1)

    # Adding circular ends (like cucumber shape)
    for bar in bars:
        bar.set_capstyle('round')  # Rounded ends on bars

    # Add the score percentage text on the bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height() / 2, f'{score}',
                va='center', color='black', fontweight='bold', fontsize=16, zorder=4)

    # Set the labels and title
    ax.set_yticks(y_pos)
    ax.set_yticklabels(criteria, fontsize=12)
    ax.set_title(f'Pronunciation Analysis for {name}', fontsize=16, fontweight='bold')

    # Customize the axis and grid
    ax.set_xlim(0, 100)
    ax.set_facecolor('white')  # Clean background
    ax.grid(False)  # Remove grid lines

    # Clean up spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Show the plot
    plt.tight_layout()
    saved_name = f'{name}.png'
    plt.savefig(saved_name)
    plt.close()

    return saved_name


# Test the function with the sample scores and name
print(create_img_corrected([80, 70, 85, 60, 40, 75], name='John Dcxvjoe'))
