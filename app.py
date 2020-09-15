import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, 
                external_stylesheets = external_stylesheets,
                suppress_callback_exceptions = True,
                meta_tags = [{"name": "viewport", 
                              "content": "width=device-width, initial-scale=1"}] 
                )

index = """
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script type="text/javascript">
            window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
            heap.load("2034103710");
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.index_string = index

app.title = "COVID-19 en Chile"

server = app.server