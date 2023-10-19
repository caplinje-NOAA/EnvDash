from dash import Dash
from dash_bootstrap_components.themes import CERULEAN

from src.components.layout import create_layout



app = Dash(external_stylesheets=[CERULEAN],prevent_initial_callbacks=True)
app.title = "Acoustic Environment Explorer"
app.layout = create_layout(app)
app.config.suppress_callback_exceptions = True
app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)


# DASH LEAFLET IS THE WAY