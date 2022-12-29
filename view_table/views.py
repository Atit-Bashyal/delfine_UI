from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go


# Create your views here.
def table(request):
    return render(request, 'view_table/tables.html', )






