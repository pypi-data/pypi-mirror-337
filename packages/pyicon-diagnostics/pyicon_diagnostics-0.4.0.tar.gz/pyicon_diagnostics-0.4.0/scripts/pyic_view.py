#!/usr/bin/env python
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import numpy as np
import xarray as xr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyicon as pyic
import cartopy.crs as ccrs
import glob
from pyicon import params
import importlib.util
if importlib.util.find_spec("ipdb"):
  from ipdb import set_trace as mybreak
import cmocean
from pyproj import Proj, CRS, Transformer

def generate_axes(asp, generate_figure=True):
    #figsize = 10,5
    figsize = 6,3
    if generate_figure:
        fig = plt.figure(figsize=figsize)
    else:
        fig = plt.gcf()
    
    figh = fig.get_figheight()
    figw  = fig.get_figwidth()
    
    x0, y0 = 0.07, 0.16
    axh0 = 0.75
    asp0 = 0.5
    axw0 = axh0*figh/figw / asp0
    ax = fig.add_subplot(position=(x0, y0, axw0, axh0))
    
    # colorbar
    daxcax = 0.02
    caxw = 0.04
    cax = fig.add_subplot(position=(x0+axw0+daxcax, y0, caxw, axh0))
    cax.set_xticks([])
    cax.yaxis.tick_right()
    cax.yaxis.set_label_position("right")

    if asp<0.5:
        axw = 1*axw0
        axh = asp/figh * (axw*figw)
        x00 = 1*x0
        y00 = y0+axh0/2.-axh/2.
    elif asp>=0.5:
        axh = 1*axh0
        axw = axh*figh/figw / asp
        x00 = x0+axw0-axw
        y00 = 1*y0
    
    ax.set_position([x00, y00, axw, axh])
    cax.set_position([x0+axw0+daxcax, y0, caxw, axh0])
    return fig, ax, cax

def get_xlim_ylim(lon_reg, lat_reg, proj, transformer):
    if proj!='None':
        #x_reg, y_reg = transformer.transform(
        #    lon_reg, lat_reg,
        #    direction='FORWARD',
        #)
        #xtest = np.linspace(x_reg[0], x_reg[1], 9)
        #ytest = np.linspace(y_reg[0], y_reg[1], 9)
        lon_test = np.linspace(lon_reg[0], lon_reg[1], 9)
        lat_test = np.linspace(lat_reg[0], lat_reg[1], 9)
        Lon_test, Lat_test = np.meshgrid(lon_test, lat_test)
        Xtest, Ytest = transformer.transform(
            Lon_test, Lat_test,
            direction='FORWARD',
        )
        xlim = np.array([Xtest.min(), Xtest.max()])
        ylim = np.array([Ytest.min(), Ytest.max()])
    else:
        xlim, ylim = lon_reg, lat_reg
    return xlim, ylim

def str_to_array(string):
  string = string.replace(' ', '')
  array = np.array(string.split(','), dtype=float)
  return array

#def get_fpath_ckdtree(data, res, path_grid, gname='auto', fpath_tgrid='auto'):
#  if path_grid == 'auto':
#    path_grid = params['path_grid']
#
#  try:
#    Dgrid = pyic.identify_grid(data, path_grid)
#  except:
#    # This doesn't always work, lets try another approach
#    try:
#      print(f"Here: {data.attrs['uuidOfHGrid']}")
#      Dgrid = pyic.identify_grid(
#        data, path_grid, uuidOfHGrid=data.attrs['uuidOfHGrid']
#        )
#    except:
#      Dgrid = dict()
#
#  if gname == "auto":
#    try:
#      gname = Dgrid["name"]
#    except KeyError:
#      gname = "none"
#
#  fpath_ckdtree = f'{path_grid}/{gname}/ckdtree/rectgrids/{gname}_res{res:3.2f}_180W-180E_90S-90N.nc'
#  print(f'fpath_ckdtree: {fpath_ckdtree}')
#  return fpath_ckdtree


def get_data(ds, var_name, it, iz, res, lon_reg, lat_reg, path_grid, do_chunking=True):
    isel_dict = dict(time=it)
    if ds[var_name].ndim==3:
      depth_name = pyic.identify_depth_name(ds[var_name])
      isel_dict[depth_name] = iz 
    else:
      depth_name = 'none'
    #else:
    #  raise ValueError(f"::: Unknown number of dimensions for {var_name}: {ds[var_name].shape}")
    da = ds[var_name]
    chunks = dict()
    if 'time' in da.dims:
        chunks = dict(time=1)
    if depth_name!='none':
        chunks[depth_name] = 1
    if do_chunking:
      da = da.chunk(**chunks)
    dai = pyic.interp_to_rectgrid_xr(
        da.isel(**isel_dict), 
        path_grid=path_grid,
        res=res,
        lon_reg=lon_reg, lat_reg=lat_reg,
        verbose=False,
        mask_out_of_range=False,
    )
    dai.attrs["depth_name"] = depth_name
    return dai.where(dai!=0.)

class view(object):
    def __init__(self, flist, path_grid, fig_size_fac=1.0):
        # Initialize Tkinter
        self.message('setup TKinter')
        root = tk.Tk()
        root.title("pyicon view")
        root.geometry("1200x800")

        self.flist = flist
        self.path_grid = path_grid
        self.fig_size_fac = fig_size_fac

        self.do_chunking = True
        self.colormaps = [
            "inferno", "viridis", "plasma", 
            "RdYlBu_r", "RdBu_r", "Blues_r", 
            "cmo.thermal", "cmo.haline", "cmo.curl", "cmo.ice", "cmo.dense",
        ]
        self.res_all = [1., 0.3, 0.1, 0.02]
        #self.proj_all = [
        #  "None", 
        #  "+proj=latlong",
        #  "+proj=stere +lat_0=90 +lon_0=0",
        #  "+proj=stere +lat_0=-90 +lon_0=0",
        #  "+proj=eqearth",
        #  "+proj=moll",
        #]
        self.proj_dict = {
          "None": "None",
          "lonlat": "+proj=latlong",
          "NorthPolar": "+proj=stere +lat_0=90 +lon_0=0",
          "SouthPolar": "+proj=stere +lat_0=-90 +lon_0=0",
          "EqualEarth": "+proj=eqearth",
          "Molleweide": "+proj=moll",
        }
        self.font_size = 6*self.fig_size_fac
        self.res = 0.3
        # lon_reg / lat_reg specify range for loaded data
        self.lon_reg = np.array([-180., 180.])
        self.lat_reg = np.array([-90., 90.])
        # xlim / ylim specify axes x and y limits 
        # (this is not the same for more complicated projections)
        self.xlim = self.lon_reg
        self.ylim = self.lat_reg
        self.it = 0
        self.iz = 0
        self.proj = self.proj_dict[list(self.proj_dict)[0]]
        if self.proj!="None":
            self.transformer = Proj.from_pipeline(self.proj)
        else:
            self.transformer = "None"

        # Opean data set
        self.message("Opening data set")
        self.load_data()

        # Default selections
        self.selected_var = tk.StringVar(value=self.var_names[0])
        self.selected_cmap = tk.StringVar(value=self.colormaps[0])
        self.color_limits = tk.StringVar(value="auto")  # Default color limits
        self.lon_lat_reg_tk = tk.StringVar(value=f"{self.lon_reg[0]},{self.lon_reg[1]},{self.lat_reg[0]},{self.lat_reg[1]}")
        self.save_fig_tk = tk.StringVar(value="./fig.pdf")
        self.selected_res = tk.StringVar(value="0.3")
        self.selected_proj = tk.StringVar(value="None")

        # Variables to store zoom area
        self.press_event = None
        self.rect = None

        # Create figure and axis
        self.message("Generating axes")
        self.fig, self.ax, self.cax = generate_axes(asp=0.5)

        #print('------')
        #print(self.fig.get_size_inches())
        #print(self.ax.get_position())

        # TK canvas
        self.message("Setting up TK")
        frame_plot = tk.Frame(root)
        frame_plot.pack(fill="both", expand=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Connect the click event to the function
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # --- 1st row
        self.message('Setup sliders')
        pady_num = 8
        frame1 = tk.Frame(root)
        frame1.pack(fill="x", pady=pady_num)

        # time slider
        btn_dec_t = tk.Button(frame1, text="-", command=lambda: self.decrease_slider(self.slider_t))
        btn_dec_t.pack(side="left")

        self.slider_t = tk.Scale(frame1, from_=0, to=len(self.ds.time)-1, 
            orient="horizontal", label="time", command=self.update_data)
        self.slider_t.pack(side="left", pady=pady_num, ipadx=160)

        btn_inc_t = tk.Button(frame1, text="+", command=lambda: self.increase_slider(self.slider_t))
        btn_inc_t.pack(side="left")

        # space inbetween
        spacer = tk.Frame(frame1, width=30)  # 10 pixels wide
        spacer.pack(side="left")
        
        # depth slider
        btn_dec_d = tk.Button(frame1, text="-", command=lambda: self.decrease_slider(self.slider_d))
        btn_dec_d.pack(side="left")

        self.slider_d = tk.Scale(frame1, from_=0, to=1,
            orient="horizontal", label="depth", command=self.update_data)
        self.slider_d.pack(side="left", pady=pady_num, ipadx=160)

        btn_inc_d = tk.Button(frame1, text="+", command=lambda: self.increase_slider(self.slider_d))
        btn_inc_d.pack(side="left")

        # --- 2nd row
        frame2 = tk.Frame(root)
        frame2.pack(fill="x", pady=pady_num)
        
        # Create dropdown menus
        self.message('Setup var dropdown')
        var_menu = ttk.Combobox(
            frame2, textvariable=self.selected_var, 
            values=list(self.ds.data_vars.keys()), state="readonly"
        )
        var_menu.pack(side="left", padx=5)
        var_menu.bind("<<ComboboxSelected>>", self.update_data)
        
        # Cmap dropdown
        self.message('Setup cmap dropdown')
        cmap_menu = ttk.Combobox(frame2, textvariable=self.selected_cmap, 
            values=self.colormaps, state="readonly")
        cmap_menu.pack(side="left", padx=5)
        cmap_menu.bind("<<ComboboxSelected>>", self.update_cmap)
        
        # Color limit entry
        self.message('Setup color limits')
        entry = tk.Entry(frame2, textvariable=self.color_limits)
        entry.pack(side="left", padx=5)
        entry.insert(0, "")  # Default value
        entry.bind("<Return>", self.update_clim)  # Update when pressing Enter

        # Checkbox for grid display
        self.do_grid = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(frame2, text="Show grid", 
            variable=self.do_grid, command=self.toggle_grid)
        self.checkbox.pack(side="left", padx=5)

        # save_fig entry
        entry = tk.Entry(frame2, textvariable=self.save_fig_tk)
        entry.pack(side="left", padx=5)
        entry.insert(0, "")  # Default value
        entry.bind("<Return>", self.save_figure)  # Update when pressing Enter

        # --- 3rd row
        frame3 = tk.Frame(root)
        frame3.pack(fill="x", pady=pady_num)

        # res entry
        self.message('Setup res dropdown')
        res_menu = ttk.Combobox(frame3, textvariable=self.selected_res, 
            values=self.res_all, state="readonly")
        res_menu.pack(side="left", padx=5)
        res_menu.bind("<<ComboboxSelected>>", self.make_new_axis)
        
        # lon_lat_reg entry
        self.message('Setup lon_reg')
        self.entry_lon_lat_reg = tk.Entry(frame3, textvariable=self.lon_lat_reg_tk)
        self.entry_lon_lat_reg.pack(side="left", padx=5)
        self.entry_lon_lat_reg.insert(0, "")  # Default value
        self.entry_lon_lat_reg.bind("<Return>", self.make_new_axis)  # Update when pressing Enter

        # Button to update data range
        self.update_range_button = ttk.Button(frame3, text="Update data range", 
            command=self.update_data_range)
        self.update_range_button.pack(side="left", padx=5)

        # Button to activate zoom mode
        self.zoom_button = ttk.Button(frame3, text="Enable Zoom", 
            command=self.activate_zoom)
        self.zoom_button.pack(side="left", padx=5)

        # Button to reset zoom
        reset_zoom_button = ttk.Button(frame3, text="Reset zoom", 
            command=self.reset_zoom)
        reset_zoom_button.pack(side="left", padx=5)

        # proj entry
        self.message('Setup proj dropdown')
        res_menu = ttk.Combobox(frame3, textvariable=self.selected_proj, 
            values=list(self.proj_dict), state="readonly")
        res_menu.pack(side="left", padx=5)
        res_menu.bind("<<ComboboxSelected>>", self.update_projection)

        # --- end tk objects

        # initial plot
        self.plot_data()
        self.canvas.draw()

        # Start Tkinter loop
        self.message('Go into mainloop')
        root.mainloop()
        return

    def message(self, message):
        print(f'pyic_view: {message}')

    # reset zoom
    def reset_zoom(self):
        self.selected_res.set("0.3")
        self.set_default_lon_lat_reg()
        self.make_new_axis()
        self.update_data()

    # for saving the figure
    def save_figure(self, *args):
        fpath = self.save_fig_tk.get()
        self.message(f'Saving figure {fpath}')
        #plt.savefig(fpath, dpi=300)
        plt.savefig(fpath, dpi=300, bbox_inches='tight')

    # for zoom
    def activate_zoom(self):
        """Activates zooming mode by connecting event handlers."""
        self.cid_press = self.canvas.mpl_connect("button_press_event", self.on_press)
        self.cid_release = self.canvas.mpl_connect("button_release_event", self.on_release)
        self.cid_motion = self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    # for zoom
    def on_press(self, event):
        """Stores the initial click position."""
        if event.xdata is not None and event.ydata is not None:
            self.press_event = (event.xdata, event.ydata)
            self.rect = self.ax.add_patch(plt.Rectangle(self.press_event, 0, 0, fill=False, color="red", linestyle="dashed"))
            self.canvas.draw()

    # for zoom
    def on_motion(self, event):
        """Updates the rectangle while dragging."""
        if self.press_event and event.xdata is not None and event.ydata is not None:
            x0, y0 = self.press_event
            width = event.xdata - x0
            height = event.ydata - y0
            self.rect.set_width(width)
            self.rect.set_height(height)
            self.canvas.draw()

    # for zoom
    def on_release(self, event):
        """Zooms into the selected rectangle and removes it."""
        if self.press_event and event.xdata is not None and event.ydata is not None:
            x0, y0 = self.press_event
            x1, y1 = event.xdata, event.ydata

            # Ensure correct ordering of coordinates
            self.ax.set_xlim(min(x0, x1), max(x0, x1))
            self.ax.set_ylim(min(y0, y1), max(y0, y1))
            #self.toggle_grid()

            # Remove the rectangle and redraw
            self.rect.remove()
            self.rect = None
            self.press_event = None
            self.canvas.draw()

            # Disable event handlers after zooming
            self.canvas.mpl_disconnect(self.cid_press)
            self.canvas.mpl_disconnect(self.cid_release)
            self.canvas.mpl_disconnect(self.cid_motion)

    def load_data(self):
        if self.flist[0].endswith('zarr'):
            self.message('Detected zarr file and switching off chunking.')
            self.do_chunking = False
        self.message('opening dataset')
        mfdset_kwargs = dict(
            combine='nested', concat_dim='time',
            data_vars='minimal', coords='minimal', 
            compat='override', join='override',
            parallel=True,
         )
        

        self.message('Data from these files is considered:')
        self.message(self.flist)
        self.ds = xr.open_mfdataset(
            self.flist, **mfdset_kwargs, 
        )
        self.message('Done opening data files')
        delvars = [
            "clon_bnds", "clat_bnds", "elon_bnds", "elat_bnds",
            "vlon_bnds", "vlat_bnds",
            "height_bnds", "height_2_bnds", "depth_bnds", "depth_2_bnds",
            "clon", "clat", "elon", "elat",
            "lev",
            "healpix",
        ]
        for var in delvars:
            try:
                self.ds = self.ds.drop_vars([var ])
            except:
                pass
        self.var_names = list(self.ds)
        self.message(f"variables in data set: {self.var_names}")
        self.var_name = self.var_names[0]

        # copy uuidOfHGrid to each variable as attribute
        for var in list(self.ds):
            try:
                self.ds[var].attrs['uuidOfHGrid'] = self.ds.attrs.get("uuidOfHGrid")
            except:
                print(f'::: Warning: No uuidOfHGrid for {var}. (Do not worry if data is on healpix grid.) :::')

        # find depth names and max number of depth dimension for all variables
        self.depth_names = dict()
        self.nzs = dict()
        delvars = []
        for var in list(self.ds):
            try:
                if self.ds[var].ndim==3:
                  self.depth_names[var] = pyic.identify_depth_name(self.ds[var])
                  self.nzs[var] = self.ds[self.depth_names[var]].size
                else:
                  self.depth_names[var] = 'none'
                  self.nzs[var] = 0
            except:
                delvars.append(var)
        self.message(f'Excluding the following variables from data set due to issues with dimension specification: {delvars}')
        self.ds = self.ds.drop_vars(delvars)

    def plot_data(self):
        # get updated limits
        self.update_lon_lat_reg()
        # get updated data
        #self.fpath_ckdtree = get_fpath_ckdtree(self.ds, self.res, self.path_grid)
        self.dai = get_data(
            self.ds, self.var_name, self.it, self.iz, 
            self.res, self.lon_reg, self.lat_reg,
            self.path_grid,
            do_chunking=self.do_chunking,
        )
        self.Lon, self.Lat = np.meshgrid(self.dai.lon.data, self.dai.lat.data)
        if self.proj=="None":
            self.X, self.Y = self.Lon, self.Lat
        else:
            self.X, self.Y = self.transformer.transform(self.Lon, self.Lat, direction='FORWARD')

        # make plot
        self.hm = pyic.shade(
            #self.X[valid], self.Y[valid], self.dai.data[valid], 
            self.X, self.Y, self.dai.to_masked_array(), 
            ax=self.ax, cax=self.cax,
            adjust_axlims=False,
        )

        ## plot the mask of land values
        #mask = self.dai.to_masked_array()
        #mask[mask!=0] = np.ma.masked
        #cmap = plt.cm.viridis
        #cmap.set_under(color='0.7')  # set color of mask
        #pyic.shade(
        #    self.X, self.Y, mask,
        #    ax=self.ax, cax=0,
        #    clim=[2,3],
        #    adjust_axlims=False,
        #    cmap=cmap,
        #)

        # set ax limits
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        # set ax labels
        if self.proj=="None" or self.proj=="+proj=latlong":
            #self.ax.set_xticks(np.arange(-180.,180.,45.))
            #self.ax.set_yticks(np.arange(-90,90,45.))
            pass
        else:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        self.update_cmap()
        self.update_clim()
        # set titles
        #self.ht_var = self.ax.set_xlabel('', fontsize=self.font_size)
        self.ht_var = self.cax.set_ylabel('', fontsize=self.font_size)
        self.ht_depth = self.ax.set_title('', loc='left', fontsize=self.font_size)
        self.ht_time = self.ax.set_title('', loc='right', fontsize=self.font_size)
        self.ht_point = self.ax.text(0., -0.15, f'', 
            transform=self.ax.transAxes, fontsize=self.font_size)
        for text in self.fig.findobj(plt.Text):
            text.set_fontsize(self.font_size)
        self.update_title()

    def make_new_axis(self, *args):

        self.res = float(self.selected_res.get())
        self.proj = self.proj_dict[self.selected_proj.get()]

        try:
          self.ax.remove()
          self.cax.remove()
        except:
          pass

        self.update_lon_lat_reg()

        asp = (self.ylim[1]-self.ylim[0])/(self.xlim[1]-self.xlim[0])
        self.fig, self.ax, self.cax = generate_axes(asp, generate_figure=False)
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)

        #print('------')
        #print(self.fig.get_size_inches())
        #print(self.ax.get_position())

        self.plot_data()
        self.canvas.draw()

    def set_default_lon_lat_reg(self):
        if self.proj=="+proj=stere +lat_0=90 +lon_0=0":
            #self.xlim = [-4660515.349812048,  4660515.349812048]
            #self.ylim = [-4658959.2511977535, 4658959.2511977535]
            self.lon_reg = [-180, 180]
            self.lat_reg = [48, 90]
            lat_reg_axlim = [60,90]
        elif self.proj=="+proj=stere +lat_0=-90 +lon_0=0":
            #self.xlim = [-5965970.154575175, 5965970.154575175]
            #self.ylim = [-5963978.177895851, 5963978.177895851]
            self.lon_reg = [-180, 180]
            self.lat_reg = [-90, -35]
            lat_reg_axlim = [-90,-50]
        else:
            self.lon_reg = [-180, 180]
            self.lat_reg = [-90, 90]
            lat_reg_axlim = self.lat_reg
        self.lon_lat_reg_tk.set(f"{self.lon_reg[0]:.3g},{self.lon_reg[1]:.3g},{self.lat_reg[0]:.3g},{self.lat_reg[1]:.3g}")
        self.xlim, self.ylim = get_xlim_ylim(
            self.lon_reg, lat_reg_axlim, self.proj, self.transformer)
        
    def update_projection(self, *args):
        self.proj = self.proj_dict[self.selected_proj.get()]
        if self.proj!="None":
            self.transformer = Proj.from_pipeline(self.proj)
        self.set_default_lon_lat_reg()
        self.make_new_axis()
    
    def update_lon_lat_reg(self, *args):
        lon_lat_reg_str = self.lon_lat_reg_tk.get()
        lon_lat_reg = str_to_array(lon_lat_reg_str)
        self.lon_reg = [lon_lat_reg[0], lon_lat_reg[1]]
        self.lat_reg = [lon_lat_reg[2], lon_lat_reg[3]]
        self.message(f'Updating lon_reg to {tuple(map(float, self.lon_reg))} and lat_reg to {tuple(map(float, self.lat_reg))}')

    def update_data_range(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        if self.proj=="None":
            self.lon_reg, self.lat_lim = xlim, ylim
            self.xlim, self.ylim = xlim, ylim
        else:
            # FIXME: This is likely not working well since data
            # interp_to_rectgrid_xr (which is currently workin in the back)
            # can only operate with simple regional limitis but not as complicated
            # as some projections require it to be
            lon_lim, lat_lim = self.transformer.transform(
                xlim, ylim, direction='INVERSE')
            self.lon_reg, self.lat_reg = lon_lim, lat_lim
            self.xlim, self.ylim = xlim, ylim
            self.message('::: Warning: "Updating data range" with more complex projections can lead to strange results. :::')

        self.lon_lat_reg_tk.set(f"{self.lon_reg[0]:.3g},{self.lon_reg[1]:.3g},{self.lat_reg[0]:.3g},{self.lat_reg[1]:.3g}")
        self.make_new_axis()

    def increase_slider(self, slider):
        slider.set(slider.get() + 1)
    
    def decrease_slider(self, slider):
        slider.set(slider.get() - 1)
    
    # Function to update plot
    def update_data(self, *args):

        # Get current slider values
        self.it = int(self.slider_t.get())
        self.iz = int(self.slider_d.get())
    
        # Get selected variable and colormap
        self.var_name = self.selected_var.get()
        cmap = self.selected_cmap.get()
        self.res = float(self.selected_res.get())

        # update depth slider
        self.slider_d.config(to=self.nzs[self.var_name]-1)
    
        self.message(f'Updating data: {self.var_name}: it = {self.it}; iz = {self.iz}')
    
        # Get data and plot
        self.update_lon_lat_reg()
        self.dai = get_data(
            self.ds, self.var_name, self.it, self.iz, 
            self.res, self.lon_reg, self.lat_reg,
            self.path_grid,
            do_chunking=self.do_chunking,
        )
        self.Lon, self.Lat = np.meshgrid(self.dai.lon, self.dai.lat)
        self.hm[0].set_array(self.dai.data.flatten())
        self.update_title()
        self.canvas.draw()
    
    def update_title(self): 
        if self.dai.depth_name!='none':
            self.ht_depth.set_text(
                f"{self.dai.depth_name} = {self.ds[self.dai.depth_name][self.iz].data}")
        self.ht_time.set_text(
            f"time = {str(self.ds.time[self.it].data)[:16]}")
        try:
            var_longname = self.ds[self.var_name].long_name
        except:
            var_longname = self.var_name
        try:
            unit = f" / {(self.ds[self.var_name].units)}"
        except:
            unit = ""
        self.ht_var.set_text(f"{var_longname}{unit}")

    def update_clim(self, *args):
        clim_str = self.color_limits.get()
        try:
            clim = self.get_clim(clim_str, self.dai)
            self.hm[0].set_clim(clim[0], clim[1])
            self.message(f'Updating clim to {tuple(map(float, clim))}')
            self.canvas.draw()
        except ValueError:
            print(f'Invalid value for clim: {clim_str}')
        if clim_str=='sym' or -clim[0]==clim[1]:
            self.selected_cmap.set('RdBu_r')
            self.update_cmap('RdBu_r')
        return 
    
    def update_cmap(self, *args):
        # update cmap
        cmap = self.selected_cmap.get()
        self.message(f"Updating cmap to {cmap}")
        if cmap.startswith('cmo'):
            cmap = cmap.split('.')[-1]
            cmap = getattr(cmocean.cm, cmap)
        else:
            cmap = getattr(plt.cm, cmap)
        cmap.set_bad('0.7')
        self.hm[0].set_cmap(cmap)
        self.canvas.draw()

    def get_clim(self, clim, data):
        # --- clim
        if isinstance(clim, str) and clim=='auto':
          clim = np.array([None, None])
        elif isinstance(clim, str) and clim=='sym':
          clim = np.array([np.abs(data).max().data])
        else:
          clim = np.array(clim.split(','), dtype=float)
        if clim.size==1:
          clim = np.array([-1, 1])*clim[0]
        if clim[0] is None:
          clim[0] = data.min().data
        if clim[1] is None:
          clim[1] = data.max().data
        return clim

    def toggle_grid(self):
        if self.do_grid.get():
            self.message('Adding grid lines')
            color='k'
            linewidth=0.5
            if self.proj=="+proj=stere +lat_0=90 +lon_0=0":
                lon_c_vals = np.arange(-180.,180., 45.)
                lat_c_vals = [40, 50, 60, 70, 80]
            elif self.proj=="+proj=stere +lat_0=-90 +lon_0=0":
                lon_c_vals = np.arange(-180.,180., 45.)
                lat_c_vals = [-30, -40, -50, -60, -70, -80]
            if self.proj=="None" or self.proj=="+proj=latlong":
                lon_c_vals = self.ax.get_xticks()
                lat_c_vals = self.ax.get_yticks()
            else: 
                lon_c_vals = np.arange(-180.,180., 45.)
                lat_c_vals = np.arange(-90.,90., 45.)
            #transformer = Proj.from_pipeline(self.proj)
            nc = 51
    
            X_c = np.empty((1,nc))
            Y_c = np.empty((1,nc))
            for nn, lat_c_val in enumerate(lat_c_vals):
              lon_c = np.linspace(-180,180,nc)
              lat_c = lat_c_val*np.ones(nc)
              if self.proj!="None":
                  x_c, y_c = self.transformer.transform(
                      lon_c, lat_c, direction='FORWARD')
              else:
                  x_c, y_c = lon_c, lat_c
              X_c = np.concatenate([X_c, x_c[np.newaxis,:]], axis=0)
              Y_c = np.concatenate([Y_c, y_c[np.newaxis,:]], axis=0)
            for nn, lon_c_val in enumerate(lon_c_vals):
              lon_c = lon_c_val*np.ones(nc)
              lat_c = np.linspace(-90,90,nc)
              if self.proj!="None":
                  x_c, y_c = self.transformer.transform(
                      lon_c, lat_c, direction='FORWARD')
              else:
                  x_c, y_c = lon_c, lat_c
              X_c = np.concatenate([X_c, x_c[np.newaxis,:]], axis=0)
              Y_c = np.concatenate([Y_c, y_c[np.newaxis,:]], axis=0)
            self.hgs = []
            for nn in range(X_c.shape[0]):
                hg, = self.ax.plot(X_c[nn,:], Y_c[nn,:], 
                    color=color, linewidth=linewidth)
                self.hgs.append(hg)
                #print(f'nn = {nn}, {self.hgs}')
        else:
            self.message('Removing grid lines')
            for hg in self.hgs:
                hg.remove()
        self.canvas.draw()

    # capture mouse click, print coordinates and data
    def on_click(self, event):
        # Avoid clicking outside the axes
        if event.xdata is not None and event.ydata is not None:  
            if self.proj!="None":
                lon_click, lat_click = self.transformer.transform(
                    event.xdata, event.ydata, 
                    direction='INVERSE',
                ) 
            else:
                lon_click, lat_click = event.xdata, event.ydata
            ind = np.argmin(
                (self.Lon.flatten()-lon_click)**2+(self.Lat.flatten()-lat_click)**2
            )
            data_click = self.dai.data.flatten()[ind]
                
            txt = f"lon:{lon_click:.2f}, lat: {lat_click:.2f}, data: {data_click:.4f}"
            self.ht_point.set_text(txt)
            print(txt)
            self.canvas.draw()

def main():
    import argparse 
    help_text = """
    Opens an interactive GUI to visualize horizontal ICON data.

    pyic_view can process data on the native ICON grid or HEALPix. For data on
    the native grid, it requires ckdtrees. These ckdtrees are looked for either
    in a directory specified by the `--path_grid` option or in 
    `pyicon/pyicon/params_user.json`.

    Usage notes:
    ------------
    Open one netcdf file:
    pyic_view icon_data_20000101T000000Z.nc
    
    Use any sort of wildcarts:
    pyic_view icon_data_20000101T*.nc 

    Open zarr archive:
    pyic_view icon_zarr_archive.zarr

    Specify path_grid:
    pyic_view icon_data_20000101T*.nc --path_grid=~/work/icon/grids

    Argument list:
    --------------
    """
    
    # --- read input arguments
    parser = argparse.ArgumentParser(description=help_text, formatter_class=argparse.RawTextHelpFormatter)

    # --- necessary arguments
    parser.add_argument('fpath_data', nargs='+', metavar='fpath_data', type=str,
                        help='Path to ICON data file.')
    parser.add_argument('--size', type=float, default=1.0,
                        help='Factor that determines the figure size')
    parser.add_argument('--path_grid', type=str, default='auto',
                        help='Path for grid information. Expects as subdirecotry the directory grid_name/ckdtree/rectgrids. Defaults to \'auto\' which means that ')
    iopts = parser.parse_args()

    #flist = glob.glob(iopts.fpath_data)
    flist = iopts.fpath_data
    flist.sort()

    # Initial plot
    View = view(flist, 
        path_grid=iopts.path_grid, 
        fig_size_fac=iopts.size,
    )

if __name__ == "__main__":
    main()
