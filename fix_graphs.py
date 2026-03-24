import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

# Fix Graph 3
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'inst_cross_clusters = producer_counts' in cell.source:
        source = cell.source
        source = source.replace('bins = range(1, 10)', 'bins = range(1, 15)')
        source = source.replace('place_counts[place_counts < 10]', 'place_counts[place_counts < 15]')
        source = source.replace('ax.set_xticks(range(1, 10))', 'ax.set_xticks(range(1, 15))')
        cell.source = source
        break

# Fix markdown for Graph 4 to explain the red axis
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and 'Graph 4' in cell.source:
        source = cell.source
        source = source.replace('2. **Institutional Sharing**: Whether the printer of the copy is different from the original printer.', 
                                '2. **Institutional Sharing (Red Line)**: Out of all the copies printed in that decade, what percentage were printed by a *new/different* printing house rather than the printing house that originally created the block?')
        cell.source = source
        break

nbf.write(nb, nb_path)
