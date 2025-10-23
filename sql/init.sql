-- Таблица типов услуг
CREATE TABLE service_types (
    type_name VARCHAR(50) PRIMARY KEY,
    complexity_coefficient NUMERIC(3,1) NOT NULL
);

-- Таблица услуг
CREATE TABLE services (
    service_code VARCHAR(10) PRIMARY KEY,
    type_name VARCHAR(50) REFERENCES service_types(type_name) ON DELETE CASCADE,
    service_name VARCHAR(100) NOT NULL UNIQUE,
    min_cost NUMERIC(10,2) NOT NULL,
    time_norm_hours NUMERIC(5,2) NOT NULL,
    hourly_rate NUMERIC(10,2) NOT NULL
);

-- Таблица партнеров
CREATE TABLE partners (
    partner_id SERIAL PRIMARY KEY,
    partner_type VARCHAR(50) NOT NULL,
    partner_name VARCHAR(100) NOT NULL UNIQUE,
    manager VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200) NOT NULL,
    inn VARCHAR(20) NOT NULL UNIQUE,
    rating INTEGER NOT NULL CHECK (rating >= 0)
);

-- Таблица заказов
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    service_code VARCHAR(10) REFERENCES services(service_code) ON DELETE CASCADE,
    partner_id INTEGER REFERENCES partners(partner_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    execution_date TIMESTAMP NOT NULL
);

-- Таблица типов материалов
CREATE TABLE material_types (
    type_name VARCHAR(50) PRIMARY KEY,
    overconsumption_percent NUMERIC(3,2) NOT NULL
);

-- Таблица материалов
CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) REFERENCES material_types(type_name) ON DELETE CASCADE,
    material_name VARCHAR(100) NOT NULL UNIQUE,
    current_price NUMERIC(10,2) NOT NULL
);

-- Таблица связей услуг и материалов
CREATE TABLE service_materials (
    service_code VARCHAR(10) REFERENCES services(service_code) ON DELETE CASCADE,
    material_id INTEGER REFERENCES materials(material_id) ON DELETE CASCADE,
    consumption_norm NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (service_code, material_id)
);