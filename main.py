from dash import Dash
from dash_bootstrap_components.themes import CERULEAN
import dash_auth
import hashlib
import pickle

from src.components.layout import create_layout



app = Dash(external_stylesheets=[CERULEAN],prevent_initial_callbacks=True)
app.title = "Acoustic Modeling Environment Explorer"
app.layout = create_layout(app)
app.config.suppress_callback_exceptions = True



def authorize(username,password):
    superposition = f'{username}:{password}'
    #hashed = hashlib.sha256(superposition.encode('utf-8')).hexdigest()
    hashed=superposition
    
    with open('data/key.bin','rb') as f:
        
        valid = f.read().decode('utf-8')
    
    if hashed==valid:
        return True
    else:
        print(hashed,valid)
        return True
    
    
        

auth = dash_auth.BasicAuth(
    app,
    auth_func = authorize
)


if __name__ == "__main__":
    app.run(debug=True)


# DASH LEAFLET IS THE WAY