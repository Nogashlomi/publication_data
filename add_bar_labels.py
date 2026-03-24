import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'inst_cross_clusters = producer_counts' in cell.source:
        source = cell.source
        if 'for x, y in zip' not in source:
            source = source.replace("ax.bar(counts.index, counts.values, color='#4a9aba', edgecolor='white')",
                                    "ax.bar(counts.index, counts.values, color='#4a9aba', edgecolor='white')\n\n# Add exact count on top of every bar\nfor x, y in zip(counts.index, counts.values):\n    ax.text(x, y + counts.max()*0.02, f'{y:,}', ha='center', va='bottom', fontsize=9, color='#2c3e50')")
            if 'ax.set_ylim' not in source:
                source = source.replace("ax.set_xticks(range(1, max_cities + 1))", "ax.set_xticks(range(1, max_cities + 1))\nax.set_ylim(0, counts.values.max() * 1.15)")
            cell.source = source
        break

nbf.write(nb, nb_path)
