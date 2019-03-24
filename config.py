# Replace with the name of your Dash app
# This will end up being part of the URL of your deployed app,
# so it can't contain any spaces, capitalizations, or special characters
#
# This name MUST match the name that you specified in the
# Dash App Manager
DASH_APP_NAME = 'cfmc-dashboard'

# Set to 'private' if you want to add a login screen to your app
# You can choose who can view the app in your list of files
# at <your-plotly-server>/organize.
# Set to 'public' if you want your app to be accessible to
# anyone who has access to your Plotly server on your network without
# a login screen.
# Set to 'secret' if you want to add a login screen, but allow it
# to be bypassed by using a secret "share_key" parameter.
DASH_APP_PRIVACY = 'public'

# Dash On-Premise is configured with either "Path based routing"
# or "Domain based routing"
# Ask your server administrator which version was set up.
# If a separate subdomain was created,
# then set this to `False`. If it was not, set this to 'True'.
# Path based routing is the default option and most On-Premise
# users use this option.
PATH_BASED_ROUTING = True
