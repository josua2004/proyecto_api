from rest_framework import generics, status
from .models import CategoriaMenu, Menu, HistorialEstados, Pedido, Promocion, MetodoDePago, MesasEstado, Mesas, Comentarios, Notificaciones, Reserva, Factura, DetallePedido
from rest_framework.response import Response
from .serializers import CategoriaMenuSerializer, UserRegisterSerializer, MenuSerializer, HistorialEstadosSerializer, PedidoSerializer, PromocionSerializer, MetodoDePagoSerializer, MesasEstadoSerializer, MesasSerializer, ComentariosSerializer, NotificacionesSerializer, ReservaSerializer, FacturaSerializer, DetallePedidoSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User

class IsAdministrador(BasePermission):
    # Permiso para verificar si el usuario pertenece al grupo "Admin"
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Admin").exists()
    
class IsCliente(BasePermission):
    # Permiso para verificar si el usuario pertenece al grupo "Cliente"
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Cliente").exists() 

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador] 
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Categoría de menú eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class CategoriaMenuListCreate(generics.ListCreateAPIView):
    queryset = CategoriaMenu.objects.all()
    serializer_class = CategoriaMenuSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

class CategoriaMenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoriaMenu.objects.all()
    serializer_class = CategoriaMenuSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Categoría de menú eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    
##############################################################################################################################

class MenuListCreate(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]

class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Usuario eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class HistorialEstadosListCreate(generics.ListCreateAPIView):
    queryset = HistorialEstados.objects.all()
    serializer_class = HistorialEstadosSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

class HistorialEstadosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialEstados.objects.all()
    serializer_class = HistorialEstadosSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Historial de estados eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class PedidoListCreate(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]

class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

##############################################################################################################################

class PromocionListCreate(generics.ListCreateAPIView):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

class PromocionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

##############################################################################################################################

class MetodoDePagoListCreate(generics.ListCreateAPIView):
    queryset = MetodoDePago.objects.all()
    serializer_class = MetodoDePagoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

class MetodoDePagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetodoDePago.objects.all()
    serializer_class = MetodoDePagoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Método de pago eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class MesasEstadoListCreate(generics.ListCreateAPIView):
    queryset = MesasEstado.objects.all()
    serializer_class = MesasEstadoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def create(self, request, *args, **kwargs):
        nombre_estado = request.data.get('nombre_estado')
        # Validación del estado antes de la creación
        if nombre_estado not in ['disponible', 'reservada', 'Disponible', 'Reservada']:
            return Response({'error': "El estado debe ser 'disponible' o 'reservada'"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MesasEstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MesasEstado.objects.all()
    serializer_class = MesasEstadoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def update(self, request, *args, **kwargs):
        # Validación adicional en la actualización
        estado = request.data.get('estado')
        if estado and estado not in ['disponible', 'reservada']:
            return Response({'error': "El estado debe ser 'disponible' o 'reservada'."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Estado de mesa eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    
##############################################################################################################################

class MesasListCreate(generics.ListCreateAPIView):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

# Detail
class MesasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Mesa eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class ComentariosListCreate(generics.ListCreateAPIView):
    queryset = Comentarios.objects.all()
    serializer_class = ComentariosSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]

# Detail
class ComentariosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentarios.objects.all()
    serializer_class = ComentariosSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Comentario eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

# ListCreate   
class NotificacionesListCreate(generics.ListCreateAPIView):
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

# Detail
class NotificacionesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Notificación eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

# ListCreate   
class ReservaListCreate(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin o Cliente
    permission_classes = [IsAuthenticated, IsAdministrador | IsCliente]

# Detail
class ReservaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Reserva eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class FacturaListCreate(generics.ListCreateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

# Detail
class FacturaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Factura eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class DetallePedidoListCreate(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

# Detail
class DetallePedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    # Permisos para acceder a la vista: autenticado y ser Admin
    permission_classes = [IsAuthenticated, IsAdministrador]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Detalle de pedido eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

##############################################################################################################################

class PedidoPorUsuario(generics.ListAPIView):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        id_cliente = self.kwargs['id_cliente']
        # Filtra los pedidos por el cliente especificado
        return Pedido.objects.filter(cliente_fk=id_cliente)

##############################################################################################################################

class ComentarioPorUsuario(generics.ListAPIView):
    serializer_class = ComentariosSerializer

    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']
        # Filtra los comentarios por el usuario especificado
        return Comentarios.objects.filter(cliente_fk=usuario_id)