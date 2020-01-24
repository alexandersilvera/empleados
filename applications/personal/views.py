from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
)
# models
from .models import Empleado
# forms
from .forms import EmpleadoForm

class InicioView(TemplateView):
    """ Vista que carga página de inicio"""
    template_name = 'inicio.html'

# Listar todos los empleados
class ListAllEmpleados(ListView):
    template_name = 'personal/list_all.html'
    paginate_by = 4
    ordering = 'first_name'
    context_object_name = 'empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', '')
        lista = Empleado.objects.filter(
            full_name__icontains=palabra_clave
        )
        return lista


class ListByAreaEmpleado(ListView):
    """ lista empleados de un area """
    template_name = 'personal/list_by_area.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name=area
        )
        return lista

class ListaEmpleadosAdmin(ListView):
    template_name = 'personal/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado


class ListEmpleadosByKword(ListView):
    """  lista empelado por palabra clave """
    template_name = 'personal/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('********************')
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name=palabra_clave
        )
        return lista


class ListHabilidadesEmpleado(ListView):
    template_name = 'personal/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        empleado = Empleado.objects.get(id=8)
        return empleado.habilidades.all()


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "personal/detail_empleado.html"

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        #toot un proceso
        context['titulo'] = 'Empleado del mes'
        return context


class SuccessView(TemplateView):
    template_name = "personal/success.html"


class EmpleadoCreateView(CreateView):
    template_name = "personal/add.html"
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy('personal_app:empleados_admin')

    def form_valid(self, form):
        # logica del proceso
        empleado = form.save(commit=False)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoUpdateView(UpdateView):
    template_name = "personal/update.html"
    model = Empleado
    fields = [
        'first_name',
        'last_name',
        'job',
        'departamento',
        'habilidades',
    ]
    success_url = reverse_lazy('personal_app:empleados_admin')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('************METODO POST****************')
        print('=====================')
        print(request.POST)
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # logica del proceso
        print('************METODO form valid****************')
        print('****************************')
        return super(EmpleadoUpdateView, self).form_valid(form)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "personal/delete.html"
    success_url = reverse_lazy('personal_app:empleados_admin')