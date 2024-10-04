# Evidencia_1
-- 1. Listado con el nombre de cada cliente y el nombre y apellido de su representante de ventas
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante  
FROM cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado;

-- 2. Clientes que han realizado pagos junto con el nombre de sus representantes de ventas
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante
FROM cliente
INNER JOIN pago ON cliente.codigo_cliente = pago.codigo_cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado;

-- 3. Clientes que no han realizado pagos junto con el nombre de sus representantes de ventas
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante
FROM cliente
LEFT JOIN pago ON cliente.codigo_cliente = pago.codigo_cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado
WHERE pago.codigo_cliente IS NULL;

-- 4. Clientes que han hecho pagos, nombre de sus representantes y la ciudad de la oficina del representante
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante, oficina.ciudad
FROM cliente
INNER JOIN pago ON cliente.codigo_cliente = pago.codigo_cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado
INNER JOIN oficina ON empleado.codigo_oficina = oficina.codigo_oficina;

-- 5. Clientes que no han hecho pagos, nombre de sus representantes y la ciudad de la oficina del representante
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante, oficina.ciudad
FROM cliente
LEFT JOIN pago ON cliente.codigo_cliente = pago.codigo_cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado
INNER JOIN oficina ON empleado.codigo_oficina = oficina.codigo_oficina
WHERE pago.codigo_cliente IS NULL;

-- 6. Dirección de las oficinas que tengan clientes en Fuenlabrada
SELECT DISTINCT oficina.linea_direccion1, oficina.linea_direccion2
FROM oficina
INNER JOIN empleado ON oficina.codigo_oficina = empleado.codigo_oficina
INNER JOIN cliente ON empleado.codigo_empleado = cliente.codigo_empleado_rep_ventas
WHERE cliente.ciudad = 'Fuenlabrada';

-- 7. Clientes y sus representantes junto con la ciudad de la oficina del representante
SELECT cliente.nombre_cliente, empleado.nombre AS nombre_representante, empleado.apellido1 AS apellido_representante, oficina.ciudad
FROM cliente
INNER JOIN empleado ON cliente.codigo_empleado_rep_ventas = empleado.codigo_empleado
INNER JOIN oficina ON empleado.codigo_oficina = oficina.codigo_oficina;

-- 8. Listado de empleados junto con el nombre de sus jefes
SELECT empleado.nombre AS nombre_empleado, jefe.nombre AS nombre_jefe
FROM empleado
INNER JOIN empleado AS jefe ON empleado.codigo_jefe = jefe.codigo_empleado;

-- 9. Listado de cada empleado, su jefe y el jefe de su jefe
SELECT e1.nombre AS nombre_empleado, e2.nombre AS nombre_jefe, e3.nombre AS nombre_jefe_jefe
FROM empleado AS e1
INNER JOIN empleado AS e2 ON e1.codigo_jefe = e2.codigo_empleado
INNER JOIN empleado AS e3 ON e2.codigo_jefe = e3.codigo_empleado;

-- 10. Clientes a los que no se les ha entregado un pedido a tiempo
SELECT cliente.nombre_cliente
FROM cliente
INNER JOIN pedido ON cliente.codigo_cliente = pedido.codigo_cliente
WHERE pedido.fecha_entrega > pedido.fecha_esperada;

-- 11. Listado de las diferentes gamas de producto que ha comprado cada cliente
SELECT cliente.nombre_cliente, gama_producto.gama
FROM cliente
INNER JOIN pedido ON cliente.codigo_cliente = pedido.codigo_cliente
INNER JOIN detalle_pedido ON pedido.codigo_pedido = detalle_pedido.codigo_pedido
INNER JOIN producto ON detalle_pedido.codigo_producto = producto.codigo_producto
INNER JOIN gama_producto ON producto.gama = gama_producto.gama
GROUP BY cliente.nombre_cliente, gama_producto.gama;
