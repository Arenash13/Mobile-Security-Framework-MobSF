from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import re_path
from DynamicAnalyzer.views.android import dynamic_analyzer as dz
from DynamicAnalyzer.views.android import (
    operations,
    report,
    tests_common,
    tests_frida)

from MobSF import utils
from MobSF.views import home
from MobSF.views.api import rest_api

from StaticAnalyzer import tests
from StaticAnalyzer.views import shared_func
from StaticAnalyzer.views.android import (
    find,
    generate_downloads,
    java,
    manifest_view,
    smali,
    view_source,
)
from StaticAnalyzer.views.windows import windows
from StaticAnalyzer.views.android import static_analyzer as android_sa
from StaticAnalyzer.views.ios import static_analyzer as ios_sa
from StaticAnalyzer.views.ios import view_source as io_view_source

from NvisoDynamicAnalysis import consumers 

# This file is used to wrap the url for HTTP and websocket protocols, 
# as HTTP app is not specified, it will search the routes in urls.py
application = ProtocolTypeRouter({'websocket' : URLRouter([
    re_path(r'^ws/frida_logs/$', consumers.FridaLogsConsumer),
])})
