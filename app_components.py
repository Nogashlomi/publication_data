import ipywidgets as widgets
import bqplot as bq
import numpy as np

from event_bus import EventBus, EventType


class KeyWordSelector:
    def __init__(self, event_bus, df):

        self.event_bus = event_bus

        keywords = df['cks'].unique().tolist()
        
        self.selector = widgets.SelectMultiple(options=keywords,
                                              layout={'height' :'100%'})


        self.app = widgets.VBox([
            self.selector
        ])


        self.selector.observe(self.on_keywords_selected, 'value')
        
    
    def on_keywords_selected(self, change):

        selected_keywords = self.selector.value

        self.event_bus.publish(EventType.KEYWORDS_SELECTED, 
                               selected_keywords)
        
        
class ImageDisplay:
    def __init__(self, df, image_path, event_bus):

        self.df = df
        self.image_path = image_path
        
        self.event_bus = event_bus
        
        self.display_box = widgets.GridBox(layout=widgets.Layout(grid_template_columns="repeat(6, 15%)", height='100%', width='100%'))


        self.app = widgets.VBox([self.display_box])

        self.event_bus.subscribe(EventType.KEYWORDS_SELECTED,
                                 self.on_keywords_selected)

    
    def on_keywords_selected(self, keyword_list):
        for child in self.display_box.children:
            if hasattr(child,'children'):
                for grandchild in child.children:
                    del grandchild
            del child
            
        
        img_widgets = []
        
        for keyword in keyword_list:
            cluster_names = self.df[self.df['cks'] == keyword]['cluster_name'].unique()
            
            for cluster_name in cluster_names:
                img_file_name = self.image_path+cluster_name+'.jpg'
                
                
                with open(img_file_name,'rb') as f:
                    img_widget = widgets.Image(value=f.read(),                                           layout=widgets.Layout(width='95%') )
                   
                    
                    img_widgets.append(img_widget)
            self.display_box.children = img_widgets



class PlotDisplay:
    def __init__(self, df, event_bus, books_df):
        self.df = df 
        self.books_df = books_df
        
        self.bins = [1470, 1490, 1510, 1530, 1550, 1570, 1590, 1610, 1630, 1650]
        self.bin_labels = {}
        for bin_i in range(len(self.bins)-1):
            low = self.bins[bin_i]
            high = self.bins[bin_i+1]
            self.bin_labels[bin_i] = str(low)+' - '+str(high)
            
        self.bin_centers = np.arange(len(self.bins)-1)
        self.book_line = np.histogram(self.books_df.year.values.astype(int), bins=self.bins, density=False)[0]
        
        self.event_bus = event_bus

        
        self.sc_x = bq.LinearScale()
        self.sc_y = bq.LinearScale()

        self.ax_x = bq.Axis(scale=self.sc_x, grid_color='rgba(100, 100, 100, 0.2)')
        self.ax_y = bq.Axis(scale=self.sc_y, orientation='vertical', grid_color='rgba(100, 100, 100, 0.2)')


        self.ax_x.num_ticks = len(self.bin_labels)
        self.ax_x.tick_values = list(self.bin_labels.keys())
        self.ax_x.tick_labels = self.bin_labels
        self.ax_x.tick_style = {'text-anchor': 'start', 'transform': 'rotate(45deg)'}
        self.lines = bq.Lines(x=np.arange(10), y=np.arange(10),
                                              scales={'x': self.sc_x, 'y': self.sc_y})

        self.book_line = bq.Lines(x=self.bin_centers, y=self.book_line,  scales={'x': self.sc_x, 'y': self.sc_y},
                                 colors=['black'],line_style='dashed', stroke_width=5)
        
        self.fig = bq.Figure(marks=[self.lines, self.book_line], axes=[self.ax_x, self.ax_y],
                             background_style={'fill': 'White'},
                             layout=widgets.Layout(width='95%', height='95%'))

        self.app = widgets.VBox([self.fig])

        self.event_bus.subscribe(EventType.KEYWORDS_SELECTED,
                                 self.on_keywords_selected)

        
                
    def on_keywords_selected(self, keyword_list):
        

        
        
        lines = []
        labels = []
        for keyword in keyword_list:
            filtered_df = self.df[self.df['cks'] == keyword]

            years = filtered_df.year.values.astype(int)

            hist = np.histogram(years, bins=self.bins, density=False)[0]
            lines.append(hist)
            labels.append(keyword)
            
        self.lines.x = self.bin_centers
        self.lines.y = lines
        self.lines.labels = labels
        self.lines.display_legend = True



class TextDisplay:
    def __init__(self, event_bus, df):
        self.event_bus = event_bus
        self.df = df

        self.display = widgets.Textarea(layout={'width': '100%', 
                                                'height': '100%'})

        self.app = self.display

        
        self.event_bus.subscribe(EventType.KEYWORDS_SELECTED,
                                 self.on_keywords_selected)

        
    def on_keywords_selected(self, keyword_list):
        new_text = ''
        
        for keyword in keyword_list:
            filtered_df = self.df[self.df['cks'] == keyword]

            n_unique_img = np.unique(filtered_df.images.values.astype(str)).shape[0]
            
            n_unique_books = np.unique(filtered_df.book.values.astype(str)).shape[0]

            n_unique_cluster_name = np.unique(filtered_df.cluster_name.values.astype(str)).shape[0]

            new_text+= keyword+'\n ------- \n imgs: '+str(n_unique_img)+' books: '+str(n_unique_books)+' clusters: '+str(n_unique_cluster_name)+'\n*****\n'

        self.display.value = new_text
            

class VisApp:
    def __init__(self, df, books_df):
        self.event_bus = EventBus()

        self.keyword_selector = KeyWordSelector(self.event_bus, df)

        self.img_app = ImageDisplay(df, r'C:\Users\nogashlomi\Library\CloudStorage\GoogleDrive-noga.shlomi@gmail.com\My Drive\images_ck_flat\', self.event_bus)

        self.plot_display = PlotDisplay(df, self.event_bus, books_df)
        self.text_display = TextDisplay(self.event_bus, df)

        self.app = widgets.GridspecLayout(n_rows=4,n_columns=4,
                                          layout=widgets.Layout(height='600px'))


        self.app[:2,0] = self.keyword_selector.app
        self.app[2:,0] = self.text_display.app
        self.app[:2,1:] = self.img_app.app
        self.app[2:,1:] = self.plot_display.app


        






        

        