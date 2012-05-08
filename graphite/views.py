import re
import os
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.sites.models import Site

def get_default_context(request):
    content_path = '/content/tasseo/'
    context = dict(
	graphite_url='http://%s' % request.get_host(),
        default_period=request.REQUEST.get('default_period', 5),
	image_path=content_path+'i',
	css_path=content_path+'c',
	js_path=content_path+'j',
	dashboards_path=content_path+'d')
    return context

def index(request):
    context = get_default_context(request)

    # if we have query params then try to extract targets
    queryParams = request.REQUEST
    metrics = []
    for target in queryParams.getlist('target'):
        metric = {}
        if target.find('alias') == 0:
            m = re.match(r'alias\((?P<target>.+),\S*"(?P<alias>.+)"\)', target)
            metric['target'] = m.group('target')
            metric['alias'] = m.group('alias')    
        else:
            metric['target'] = target
            metric['alias'] = target    
        if queryParams.get('warning'):
            metric['warning'] = queryParams.get('warning')
        if queryParams.get('critical'):
            metric['critical'] = queryParams.get('critical')
        if queryParams.get('unit'):
            metric['unit'] = queryParams.get('unit')
        metrics.append(metric)
    if len(metrics) > 0:
        context['metrics'] = metrics
    else:
        # no metrics in the query string so just list all the dashboards
        dashboards = []
        for f in os.listdir(settings.CONTENT_DIR + '/tasseo/d/'):
            if f.endswith('.js'):
                dashboards.append(f.replace('.js', ''))
        context["dashboards"] = dashboards

    return render_to_response("tasseo.html", context)

def dashboard(request, dashboard):
    context = get_default_context(request)
    context['dashboard'] = dashboard
    return render_to_response("tasseo.html", context)
