// Insertar roles
INSERT INTO `riego`.`api_rol` (`id`, `categoria`) VALUES ('1', 'Administrador');
INSERT INTO `riego`.`api_rol` (`id`, `categoria`) VALUES ('2', 'Usuario');
INSERT INTO `riego`.`api_rol` (`id`, `categoria`) VALUES ('3', 'Desarrollador');

// Insertar datos api_raspberry
INSERT INTO `riego`.`api_raspberry` (`id`, `codigo`, `ruta`, `area`, `latitud`, `longitud`, `bateria`) VALUES ('1', 'r001','', '62.5', '-16.3988900', '-71.5350000', '78');
INSERT INTO `riego`.`api_raspberry` (`id`, `codigo`, `ruta`, `area`, `latitud`, `longitud`, `bateria`) VALUES ('2', 'r002','', '12.5', '-16.4998900', '-70.5350000', '60');
INSERT INTO `riego`.`api_raspberry` (`id`, `codigo`, `ruta`, `area`, `latitud`, `longitud`, `bateria`) VALUES ('3', 'r003','', '5.2', '-16.8955900', '-69.5350000', '55');
INSERT INTO `riego`.`api_raspberry` (`id`, `codigo`, `ruta`, `area`, `latitud`, `longitud`, `bateria`) VALUES ('4', 'r004','', '42.7', '-16.5088900', '-72.5350000', '71');


// Insertar ESP32Humedad
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('1', 'esp32_001', '55', '-16.3977', '-71.5351', '1');
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('2', 'esp32_002', '52', '-16.4177', '-71.5251', '1');
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('3', 'esp32_003', '98', '-16.4277', '-71.5151', '1');
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('4', 'esp32_004', '85', '-16.4377', '-71.5051', '1');
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('5', 'esp32_005', '70', '-16.4477', '-71.4951', '2');
INSERT INTO `riego`.`api_esp32humedad` (`id`, `codigo`, `bateria`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('6', 'esp32_006', '33', '-16.4577', '-71.5851', '2');


// Insertar usuarios (POSTMAN)

// Insertar esp32control
INSERT INTO `riego`.`api_esp32control` (`id`, `codigo`, `area`, `bateria`, `descarga`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('1', 'c_001', '40.5', '85', '10.0', '-16.4579', '-71.5859', '1');
INSERT INTO `riego`.`api_esp32control` (`id`, `codigo`, `area`, `bateria`, `descarga`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('2', 'c_002', '12', '78', '8', '-16.4679', '-71.5968', '1');
INSERT INTO `riego`.`api_esp32control` (`id`, `codigo`, `area`, `bateria`, `descarga`, `latitud`, `longitud`, `idRaspberry_id`) VALUES ('3', 'c_003', '12.5', '68', '12', '-16.4555', '-71.6060', '2');

// Insertar programa
INSERT INTO `riego`.`api_programa` (id, fecha, semana, hora_inicio, hora_fin, kc, volumen_ha, idEsp32_id)
VALUES
(1, '2024-07-01', 27, '08:00:00', '10:00:00', 0.45, 150.0, 1),
(2, '2024-07-02', 27, '09:00:00', '11:00:00', 0.50, 160.0, 1),
(3, '2024-07-03', 27, '10:00:00', '12:00:00', 0.55, 170.0, 1),
(4, '2024-07-04', 27, '11:00:00', '13:00:00', 0.60, 180.0, 1),
(5, '2024-07-05', 27, '12:00:00', '14:00:00', 0.65, 190.0, 1),
(6, '2024-07-06', 27, '08:00:00', '10:00:00', 0.70, 200.0, 2),
(7, '2024-07-07', 27, '09:00:00', '11:00:00', 0.75, 210.0, 2),
(8, '2024-07-08', 28, '10:00:00', '12:00:00', 0.80, 220.0, 2),
(9, '2024-07-09', 28, '11:00:00', '13:00:00', 0.85, 230.0, 2),
(10, '2024-07-10', 28, '12:00:00', '14:00:00', 0.90, 240.0, 2);




