from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
import re
from .models import CategoriaMenu, Menu, HistorialEstados, Pedido, Promocion, MetodoDePago, MesasEstado, Mesas, Comentarios, Notificaciones, Reserva, Factura, DetallePedido
from django.contrib.auth.models import User, Group
from rest_framework.response import Response


class UserRegisterSerializer(serializers.ModelSerializer):
    # Campo 'role' se define como solo escritura
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Campos que se incluirán en la serialización
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'role')
        
    def validate_password(self, value):
        # Validación para asegurar que la contraseña tenga al menos 6 caracteres
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return value

    def create(self, validated_data):
        # Extraer el rol del usuario del conjunto de datos validados
        role = validated_data.pop('role')
        # Crear una instancia de User con los datos validados
        user = User(**validated_data)
        # Establecer la contraseña encriptada
        user.set_password(validated_data['password'])
        # Guardar el usuario en la base de datos
        user.save()

        # Asignar el rol al grupo correspondiente si existe
        if role: 
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"El role '{role}' no existe")

        return user
    
    def update(self, instance, validated_data):
        # Actualizar los campos del usuario con los datos proporcionados
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Si se proporciona una nueva contraseña, establecerla y guardar el usuario
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()  
    
        return instance

###################################################################################################################
class CategoriaMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMenu
        # Incluir todos los campos del modelo CategoriaMenu
        fields = '__all__'
  
    def validate_nombre(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
   
        # Validar que el nombre solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("Este campo solo debe contener letras y espacios.")
        return value
        
    def validate_descripcion(self, value):
        # Validar que la descripción solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("Este campo solo debe contener letras y espacios.")
        return value

###################################################################################################################
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        # Incluir todos los campos del modelo Menu
        fields = '__all__'
        
    def validate_nombre(self, value):
        # Validar que el nombre del menú no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre del menú no puede estar vacío.")
        # Validar que el nombre tenga al menos 3 caracteres
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del menú debe tener al menos 3 caracteres.")
        # Validar que el nombre solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("Este campo solo debe contener letras y espacios.")
        return value 
    
    def validate_precio(self, value):
        # Validar que el precio del menú sea un valor positivo
        if value <= 0:
            raise serializers.ValidationError("El precio del menú debe ser un valor positivo.")
        return value

    def validate_categoria(self, value):
        # Validar que la categoría no esté vacía
        if not value.strip():
            raise serializers.ValidationError("La categoría no puede estar vacía.")
        return value
    
    def validate_descripcion(self, value):
        # Validar que la descripción solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("Este campo solo debe contener letras y espacios.")
        return value
  
################################################################################################################### 
class HistorialEstadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEstados
        # Incluir todos los campos del modelo HistorialEstados
        fields = '__all__'

    def validate_estado(self, value):
        # Validar que el estado esté dentro de los estados permitidos
        validate_states = ['preparación', 'enviado', 'entregado']
        if value not in validate_states:
            raise serializers.ValidationError("Estado no válido. Opciones: 'preparación', 'enviado', 'entregado'.")
        return value
        
    def cambiar_estado(self, nuevo_estado):
        # Cambiar el estado del historial si el nuevo estado es válido
        if nuevo_estado not in dict(self.ESTADOS_CHOICES):
            raise ValueError("Estado no válido.")
        self.estado = nuevo_estado
        self.fecha_cambio = timezone.now()  # Actualizar la fecha del cambio
        self.save()  # Guardar los cambios en la base de datos

###################################################################################################################
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        # Incluir todos los campos del modelo Pedido
        fields = '__all__'

    def validate_precio(self, value):
        # Validar que el precio sea un valor mayor a cero
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return value

    
################################################################################################################### 
    
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        # Incluir todos los campos del modelo Promocion
        fields = '__all__'

    def validate(self, attrs):
        # Validar que el descuento esté entre 0 y 100
        if not (0 <= attrs['descuento'] <= 100):
            raise serializers.ValidationError({"descuento": "El descuento debe estar entre 0 y 100."})
        
        # Validar que la fecha de vencimiento no sea en el pasado
        if attrs['fecha_vencimiento'] < timezone.now():
            raise serializers.ValidationError({"fecha_vencimiento": "La fecha de vencimiento no puede ser en el pasado."})

        return attrs
        
###################################################################################################################   

class MetodoDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoDePago
        # Incluir todos los campos del modelo MetodoDePago
        fields = '__all__'

    def validate_total_compra(self, value):
        # Validar que el total de la compra sea un número positivo
        if value <= 0:
            raise serializers.ValidationError("El total de la compra debe ser un número positivo.")
        return value

    def validate(self, attrs):
        # Validar que el tipo de pago no esté vacío
        if attrs.get('tipo_pago') == "":
            raise serializers.ValidationError({"tipo_pago": "El tipo de pago no puede estar vacío."})
        return attrs
    
################################################################################################################### 
    
class MesasEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesasEstado
        # Incluir campos específicos del modelo MesasEstado
        fields = ['id', 'nombre_estado']
    
    def validate_estado(self, value):
        # Validar que el estado sea 'disponible' o 'reservada' (teniendo en cuenta mayúsculas)
        if value not in ['disponible', 'reservada', 'Disponible', 'Reservada']:
            raise serializers.ValidationError("El estado debe ser 'disponible' o 'reservada'.")
        return value
        
###################################################################################################################

class MesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesas
        # Incluir todos los campos del modelo Mesas
        fields = '__all__'

    def validate_capacidad_mesa(self, value): 
        # Validar que la capacidad de la mesa sea mayor que cero
        if value <= 0:
            raise serializers.ValidationError("La capacidad de la mesa debe ser mayor que cero") 
        return value 
    
    def validate_numero_mesa(self, value): 
        # Verificar si ya existe una mesa con el mismo número
        if Mesas.objects.filter(numero_mesa=value).exists(): 
            raise serializers.ValidationError("Ya existe una mesa con este número") 
        return value 
    
    def validate_disponibilidad_mesa(self, value): 
        # Validar que la mesa no esté reservada
        if value.estado == 'Reservada': 
            raise serializers.ValidationError("No se puede agregar una mesa que esté reservada") 
        return value

################################################################################################################### 
    
class ComentariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios
        fields = '__all__'
    
    def validate_comentario(self, value): 
        if not value: raise serializers.ValidationError("El comentario no puede estar vacío") 
        if len(value) > 500: # Limitar longitud del comentario 
            raise serializers.ValidationError("El comentario no puede exceder los 500 caracteres") 
        return value 
    
    def validate_calificacion(self, value): 
        if value is None: raise serializers.ValidationError("La calificación es obligatoria") 
        if value < 1 or value > 5: raise serializers.ValidationError("La calificación debe estar entre 1 y 5") 
        return value 
    
    def validate_id_menu_comentarios(self, value): 
        if not Menu.objects.filter(id=value.id).exists(): 
            raise serializers.ValidationError("El menú especificado no existe") 
        return value
        
###################################################################################################################

class NotificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = '__all__'

    def validate_mensaje(self, value): 
        if not value: 
            raise serializers.ValidationError("El mensaje no puede estar vacío.") 
        if len(value) > 500: 
            raise serializers.ValidationError("El mensaje no puede exceder los 500 caracteres") 
        return value 
    
################################################################################################################### 
    
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        # Incluir todos los campos del modelo Reserva
        fields = '__all__'

    def validate(self, attrs):
        # Validar que la fecha de reserva no sea en el pasado
        if attrs['fecha_reserva'] < timezone.now():
            raise serializers.ValidationError({"fecha_reserva": "La fecha de reserva no puede ser en el pasado."})
        
        # Verificar que la mesa especificada exista
        if not Mesas.objects.filter(id=attrs['id_mesa'].id).exists():
            raise serializers.ValidationError({"id_mesa": "La mesa especificada no existe."})

        return attrs
        
###################################################################################################################  

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        # Incluir todos los campos del modelo Factura
        fields = '__all__'
        # Definir campos de solo lectura
        read_only_fields = ['fecha_emision', 'total_factura']
        
    def validate_usuario(self, value):
        # Validar que el usuario no sea nulo
        if value is None:
            raise serializers.ValidationError("El usuario no puede ser nulo")
        return value
        
    def validate_detalles_pedido(self, value):
        # Validar que haya al menos un detalle de pedido
        if not value.exists():
            raise serializers.ValidationError("Debe haber al menos un detalle de pedido.")
        return value   
    
    def to_representation(self, instance):
        # Personalizar la representación de la factura
        representation = super().to_representation(instance)
        
        # Calcular el total de la factura sumando los detalles del pedido
        total = sum(detalle.total for detalle in instance.detallepedido_set.all())
        representation['total_factura'] = total
        
        return representation

    def create(self, validated_data):
        # Crear una nueva factura
        factura = Factura.objects.create(**validated_data)
        
        # Calcular el total de la factura y guardarlo
        factura.total_factura = sum(detalle.total for detalle in factura.detallepedido_set.all())
        factura.save()
        
        return factura    

###################################################################################################################  

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        # Incluir todos los campos del modelo DetallePedido
        fields = '__all__'
        # Definir campos de solo lectura
        read_only_fields = ['detalle_pedido_creado', 'detalle_pedido_actualizado', 'subtotal', 'iva', 'total']

    def validate(self, data):
        # Validar los detalles del pedido
        cantidad = data.get('cantidad', 1)
        id_menu = data.get('id_menu')
        id_promocion = data.get('id_promocion')
        menu = Menu.objects.get(id=id_menu.id)
        subtotal = menu.precio * cantidad 

        # Aplicar promoción si está presente y es válida
        if id_promocion:
            promocion = Promocion.objects.filter(id=id_promocion.id, fecha_vencimiento__gt=datetime.now()).first()
            if promocion:
                descuento = promocion.descuento / 100 
                subtotal = subtotal * (1 - descuento)  
            else:
                raise serializers.ValidationError("La promoción no es válida o ha expirado.")

        # Calcular IVA y total
        tasa_iva = 0.13
        iva = round(subtotal * tasa_iva, 2)
        total = round(subtotal + iva, 2)

        # Almacenar cálculos en los datos
        data['subtotal'] = subtotal
        data['iva'] = iva
        data['total'] = total
        return data

    def create(self, validated_data):
        # Crear un nuevo detalle de pedido
        return DetallePedido.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar los campos del detalle de pedido
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.id_pedido = validated_data.get('id_pedido', instance.id_pedido)
        instance.id_menu = validated_data.get('id_menu', instance.id_menu)
        instance.factura = validated_data.get('factura', instance.factura)
        instance.id_promocion = validated_data.get('id_promocion', instance.id_promocion)

        # Validar y calcular valores
        validated_data = self.validate(validated_data)
        instance.subtotal = validated_data['subtotal']
        instance.iva = validated_data['iva']
        instance.total = validated_data['total']

        # Guardar cambios
        instance.save()
        return instance