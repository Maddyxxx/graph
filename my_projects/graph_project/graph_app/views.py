import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import VectorForm, GraphForm
from .models import Graph, Vector
from core import calculate, resize


class MainPage(View):

    def get(self, request):
        graph_data, results = [], []

        result_id = 0  # для корректного построения стрелок на странице

        graphs = Graph.objects.all()
        vector_form = VectorForm()
        graph_form = GraphForm()

        for graph in graphs:
            vectors = [i.vector for i in Vector.objects.filter(graph=graph)]

            resize_vec = resize(vectors)

            graph_data.append({
                'vectors': resize_vec,
                'operation': graph.operation,
            })

        deep = len(graph_data) - 1  # глубина графа

        for num in range(deep):
            result = calculate(data=graph_data[num]['vectors'], operation=graph_data[num]['operation'])
            result_id += len(graph_data[num]['vectors']) + 1
            results.append({'result': str(result), 'result_id': result_id})
            graph_data[num + 1]['vectors'].append(str(result))

        result = calculate(data=graph_data[deep]['vectors'], operation=graph_data[deep]['operation'])
        results.append({'result': result, 'result_id': result_id + len(graph_data[deep]['vectors']) + 1})

        for num in range(deep - 1):  # исключительно для корректрого отображения на странице
            graph_data[num + 1]['vectors'].remove(graph_data[num + 1]['vectors'][-1])

        return render(request, 'graphs/main_page.html', {
            'graph_form': graph_form,
            'vector_form': vector_form,
            'vectors': json.dumps(graph_data),
            'results': json.dumps(results),
        })

    def post(self, request):
        vector_form = VectorForm(request.POST)
        graph_form = GraphForm(request.POST)

        if vector_form.is_valid():
            Vector.objects.create(**vector_form.cleaned_data)
            return HttpResponseRedirect(f'/graph/main/')
        elif graph_form.is_valid():
            Graph.objects.create(**graph_form.cleaned_data)
            return HttpResponseRedirect(f'/graph/main/')

        return render(request, 'graphs/main_page.html', {
            'graph_form': graph_form, 'vector_form': vector_form})
