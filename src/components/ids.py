import uuid

MAP = "map"
MAP_FIG = 'map-fig'
BB_MAP_LAYER = 'bath-map-layer'
SSP_MAP_LAYER = 'ssp-map-layer'
SEABED_MAP_LAYER = 'seabed-map-layer'
TRANS_MAP_LAYER = 'transect-map-layer'
BATH_PLOT ='bath-plot'

SSP_PLOT = 'ssp-plot'
LAT_INPUT = 'latitude-input'
LON_INPUT = 'longitude-input'
GET_DATA_BUTTON='get-data-button'
BB_KM = 'bounding-box-kilometers'
BATH_SOURCE_DROPDOWN = 'bath-source-dropdown'
STRIDE_SLIDER = 'stride-slider'
TAB_SPINNER='tab-loading-spinner'
TAB_SPINNER_SECONDARY='secondary-tab-loading-spinner'
BATH_TAB_CONTENT = 'bath-tab-content'
TRANSECT_CONTENT = 'transect-content'
SSP_TAB_CONTENT = 'ssp-tab-content'
SEABED_TAB_CONTENT = 'seabed-tab-content'

BATH_ERROR = 'bath-error'
ALERT = 'alert-div'

SSP_MONTH_DROPDOWN ='SSP-month-dropdown'
SSP_EXCLUDE_DROPDOWN = 'ssp-include'
OPTION_DIV = 'options-div'
FIGURE_DIV = 'figure-div'
TAB_CONTENT_DIV = 'tab-content-div'
TABS ='tabs'

TRANSECT_DROPDOWN='transect-dropdown'
TRANSECT_COLLAPSE='transect-collapse'
TRANSECT_COLLAPSE_BUTTON='transect-collapse-button'

TRANSECT_INPUT = 'transect-input'
# transect inputs
LAT_INPUT_START = {"type":TRANSECT_INPUT,"parameter":'lat-start'}
LAT_INPUT_END = {"type":TRANSECT_INPUT,"parameter":'lat-end'}
LON_INPUT_START = {"type":TRANSECT_INPUT,"parameter":'lon-start'}
LON_INPUT_END = {"type":TRANSECT_INPUT,"parameter":'lon-end'}
RADIAL_STEP_INPUT = {"type":TRANSECT_INPUT,"parameter":'radial-step'}
AZ_INPUT = {"type":TRANSECT_INPUT,"parameter":'single-azimuth'}



TRANS_INPUTS_DIV = 'transect-inputs-div'
PLOT_TRANSECTS_BUTTON_S = 'plot-transects-single'
PLOT_TRANSECTS_BUTTON_S_AZ = 'plot-transects-single-az'
PLOT_TRANSECTS_BUTTON_M = 'plot-transects-multiple'
TRANSECT_PLOT = 'transect-figure-plot'

META_DATA_STORE='dachshunds-are-the-best-dogs'
BATH_INPUTS_STORE = 'bath-inputs-store'
SSP_INPUTS_STORE = 'ssp-inputs-store'
SEABED_INPUTS_STORE = 'seabed-inputs-store'

SEABED_SLIDER = 'seabed-slider'
SEABED_TABLE = 'seabed-table'

DOWNLOAD_CANVAS_BUTTON = 'download-canvas-button'
DOWNLOAD_CANVAS = 'download-canvas'
DOWNLOAD_BATH_BUTTON = 'download-bath-button'
BATH_INPUTS_DISPLAY = 'bath-inputs-display'

SSP_FILE_TYPE_DROPDOWN = 'ssp-file-type-dropdown'
SSP_DOWNLOAD_BUTTON = 'ssp-download-button'
SSP_DOWNLOAD = 'ssp-download'
SSP_INPUTS_DISPLAY = 'ssp-inputs-display'
SEABED_DOWNLOAD_BUTTON = 'seabed-download-button'
SEABED_DOWNLOAD = 'seabed-download'
SEABED_INPUTS_DISPLAY = 'seabed-inputs-display'

def SSP_MARKER(loc):
    return {'type':'WOA-data-marker','location':loc}

def SSP_MARKER_TOOLTIP(loc):
    return {'type':'WOA-data-marker-tooltip','location':loc}

def unique()->str:
    return str(uuid.uuid1())
    
    
    
    