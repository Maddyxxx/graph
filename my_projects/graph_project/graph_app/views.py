import json
from django.shortcuts import render
from django.views import View
from .models import Graph
from core import calculate


class MainPage(View):

    def get(self, request):
        vectors = []
        graphs = Graph.objects.all()
        for graph in graphs:
            vectors.append(graph.vector)

        result = calculate(data=list(vectors), number=2)
        vectors.append(result)
        return render(request, 'graphs/main_page.html', {'vectors': json.dumps(vectors), 'len_vectors': len(vectors)})
