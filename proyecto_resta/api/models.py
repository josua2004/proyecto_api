from django.db import models
from django.contrib.auth.models import User

class CategoriaMenu(models.Model):
    categoria_creada = models.DateTimeField(auto_now_add=True)
    categoria_actualizada = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
####################################################################################

class Menu(models.Model):
    menu_creado = models.DateTimeField(auto_now_add=True)
    menu_actualizado = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    categoria_fk = models.ForeignKey(CategoriaMenu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

####################################################################################

class HistorialEstados(models.Model):   
    historial_creado = models.DateTimeField(auto_now_add=True)
    historial_actualizado = models.DateTimeField(auto_now=True)
    ESTADO_PREPARACION = 'preparación'
    ESTADO_ENVIADO = 'enviado'
    ESTADO_ENTREGADO = 'entregado'

    ESTADOS_CHOICES = [
        (ESTADO_PREPARACION, 'Preparación'),
        (ESTADO_ENVIADO, 'Enviado'),
        (ESTADO_ENTREGADO, 'Entregado')
    ]

    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=ESTADO_PREPARACION)
    
    def __str__(self):
        return f"Historial {self.pk} - Estado {self.estado}"

####################################################################################

class Pedido(models.Model):
    pedido_creado = models.DateTimeField(auto_now_add=True)
    pedido_actualizado = models.DateTimeField(auto_now=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_fk = models.ForeignKey(HistorialEstados, on_delete=models.CASCADE)
    cliente_fk = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Pedido {self.pk} - Fecha {self.fecha_pedido}"

####################################################################################

class Promocion(models.Model):
    promocion_creado = models.DateTimeField(auto_now_add=True)
    promocion_actualizado = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    descuento = models.IntegerField()
    fecha_vencimiento = models.DateTimeField()
    menu_fk = models.ForeignKey(Menu, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Promoción {self.nombre} - {self.id_menu}"

####################################################################################

class MetodoDePago(models.Model):
    metodo_pago_creado = models.DateTimeField(auto_now_add=True)
    metodo_pago_actualizado = models.DateTimeField(auto_now=True)
    tipo_pago = models.CharField(max_length=50)  
    fecha_compra = models.DateField()
    total_compra = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.tipo_pago

####################################################################################

class MesasEstado(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('reservada', 'Reservada'),
        ('Disponible', 'disponible'),
        ('Reservada', 'reservada'),
    ]
    estado_mesa_creado = models.DateTimeField(auto_now_add=True)
    estado_mesa_actualizado = models.DateTimeField(auto_now=True)
    nombre_estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.nombre_estado

####################################################################################

class Mesas(models.Model):
    mesa_creada = models.DateTimeField(auto_now_add=True)
    mesa_actualizada = models.DateTimeField(auto_now=True)
    numero_mesa = models.IntegerField()
    capacidad_mesa = models.IntegerField()
    estado_mesa_fk = models.ForeignKey(MesasEstado, on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.numero_mesa)

####################################################################################

class Comentarios(models.Model):
    comentario_creado = models.DateTimeField(auto_now_add=True)
    comentario_actualizado = models.DateTimeField(auto_now=True)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    menu_fk = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cliente_fk = models.ForeignKey(User, on_delete=models.CASCADE)  
   
    def __str__(self):
        return str(self.comentario)

####################################################################################

class Notificaciones(models.Model):
    notificacion_creada = models.DateTimeField(auto_now_add=True)
    notificacion_actualizada = models.DateTimeField(auto_now=True)
    mensaje = models.TextField()
    leido = models.BooleanField()
    cliente_fk = models.ForeignKey(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.mensaje)

####################################################################################

class Reserva(models.Model):
    reserva_creada = models.DateTimeField(auto_now_add=True)
    reserva_actualizada = models.DateTimeField(auto_now=True)
    mesa_fk = models.ForeignKey(Mesas, on_delete=models.CASCADE)
    metodo_pago_fk = models.ForeignKey(MetodoDePago, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()
    cliente_fk = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva {self.pk}"

####################################################################################

class Factura(models.Model):
    fecha_emision = models.DateTimeField(auto_now_add=True) 
    factura_actualizada = models.DateTimeField(auto_now=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    metodo_pago_fk = models.ForeignKey(MetodoDePago, on_delete=models.CASCADE) 
    mesa_fk = models.ForeignKey(Mesas, on_delete=models.CASCADE)  
    cliente_fk = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Factura {self.pk} - Total {self.total_factura} - MetodoDePago {self.metodo_pago.tipo_pago}"

####################################################################################

class DetallePedido(models.Model):
    detalle_pedido_creado = models.DateTimeField(auto_now_add=True)
    detalle_pedido_actualizado = models.DateTimeField(auto_now=True)
    cantidad = models.IntegerField()
    subtotal = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()
    pedido_fk = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    menu_fk = models.ForeignKey('Menu', on_delete=models.CASCADE)
    factura_fk = models.ForeignKey('Factura', on_delete=models.CASCADE, null=True, blank=True)
    promocion_fk = models.ForeignKey('Promocion', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Total: ${self.total}"