from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import re
from sqlalchemy.exc import IntegrityError, OperationalError
from math import ceil
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Для flash-сообщений
db = SQLAlchemy(app)

# Модель для типов услуг
class ServiceType(db.Model):
    __tablename__ = 'service_types'
    type_name = db.Column(db.String(50), primary_key=True)
    complexity_coefficient = db.Column(db.Numeric(3, 1), nullable=False)
    services = db.relationship('Service', backref='service_type', lazy=True)

# Модель для услуг
class Service(db.Model):
    __tablename__ = 'services'
    service_code = db.Column(db.String(10), primary_key=True)
    type_name = db.Column(db.String(50), db.ForeignKey('service_types.type_name'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False, unique=True)
    min_cost = db.Column(db.Numeric(10, 2), nullable=False)
    time_norm_hours = db.Column(db.Numeric(5, 2), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    orders = db.relationship('Order', backref='service', lazy=True)
    materials = db.relationship('ServiceMaterial', backref='service', lazy=True)

# Модель для партнеров
class Partner(db.Model):
    __tablename__ = 'partners'
    partner_id = db.Column(db.Integer, primary_key=True)
    partner_type = db.Column(db.String(50), nullable=False)
    partner_name = db.Column(db.String(100), nullable=False, unique=True)
    manager = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    inn = db.Column(db.String(20), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='partner', lazy=True)

# Модель для заказов
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    service_code = db.Column(db.String(10), db.ForeignKey('services.service_code'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.partner_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    execution_date = db.Column(db.DateTime, nullable=False)

# Модель для типов материалов
class MaterialType(db.Model):
    __tablename__ = 'material_types'
    type_name = db.Column(db.String(50), primary_key=True)
    overconsumption_percent = db.Column(db.Numeric(3, 2), nullable=False)
    materials = db.relationship('Material', backref='material_type', lazy=True)

# Модель для материалов
class Material(db.Model):
    __tablename__ = 'materials'
    material_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), db.ForeignKey('material_types.type_name'), nullable=False)
    material_name = db.Column(db.String(100), nullable=False, unique=True)
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    service_materials = db.relationship('ServiceMaterial', backref='material', lazy=True)

# Модель для связи услуг и материалов
class ServiceMaterial(db.Model):
    __tablename__ = 'service_materials'
    service_code = db.Column(db.String(10), db.ForeignKey('services.service_code'), primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), primary_key=True)
    consumption_norm = db.Column(db.Numeric(10, 2), nullable=False)

# Функция расчета себестоимости услуги
def calculate_service_cost(service_code):
    try:
        service = Service.query.filter_by(service_code=service_code).first()
        if not service:
            logger.error(f"Service not found: {service_code}")
            return -1

        labor_cost = float(service.time_norm_hours * service.hourly_rate)
        material_cost = 0
        service_materials = ServiceMaterial.query.filter_by(service_code=service_code).all()
        if not service_materials:
            logger.error(f"No materials found for service: {service_code}")
            return -1

        for sm in service_materials:
            material = Material.query.filter_by(material_id=sm.material_id).first()
            if not material:
                logger.error(f"Material not found for service material: {sm.material_id}")
                return -1
            material_cost += float(sm.consumption_norm * material.current_price)

        total_cost = labor_cost + material_cost
        return round(total_cost, 2)
    except Exception as e:
        logger.error(f"Error calculating service cost for {service_code}: {str(e)}")
        return -1

# Функция расчета количества материала
def calculate_material_quantity(service_type, material_type, quantity, service_params):
    try:
        # Проверка входных параметров
        if not isinstance(quantity, int) or quantity <= 0:
            logger.error(f"Invalid quantity: {quantity}")
            return -1
        if not isinstance(service_params, (int, float)) or service_params <= 0:
            logger.error(f"Invalid service_params: {service_params}")
            return -1

        # Получение данных о типе услуги
        service_type_data = ServiceType.query.filter_by(type_name=service_type).first()
        if not service_type_data:
            logger.error(f"Service type not found: {service_type}")
            return -1

        # Получение данных о типе материала
        material_type_data = MaterialType.query.filter_by(type_name=material_type).first()
        if not material_type_data:
            logger.error(f"Material type not found: {material_type}")
            return -1

        # Расчет количества материала на одну услугу
        base_quantity = service_params * float(service_type_data.complexity_coefficient)

        # Учет перерасхода
        overconsumption = float(material_type_data.overconsumption_percent)
        total_quantity = base_quantity * quantity * (1 + overconsumption)

        # Округление вверх до целого
        return ceil(total_quantity)
    except Exception as e:
        logger.error(f"Error calculating material quantity: {str(e)}")
        return -1

# Создание таблиц
try:
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
except OperationalError as e:
    logger.error(f"Database connection error: {str(e)}")
    raise

# Главная страница (список партнеров)
@app.route('/')
def index():
    try:
        partners = Partner.query.all()
        return render_template('index.html', partners=partners)
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return render_template('index.html', partners=[])

# Список партнеров
@app.route('/partners')
def partners():
    try:
        partners = Partner.query.all()
        return render_template('partners.html', partners=partners)
    except Exception as e:
        logger.error(f"Error loading partners: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return render_template('partners.html', partners=[])

# Форма создания заказа
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        try:
            partner_id = request.form['partner_id']
            service_code = request.form['service_code']
            quantity = request.form['quantity']
            execution_date = request.form['execution_date']

            # Валидация данных
            if not partner_id or not service_code or not quantity or not execution_date:
                flash('Все поля обязательны для заполнения.', 'error')
                return redirect(url_for('order'))

            quantity = int(quantity)
            if quantity <= 0:
                flash('Количество должно быть положительным числом.', 'error')
                return redirect(url_for('order'))

            order = Order(
                partner_id=partner_id,
                service_code=service_code,
                quantity=quantity,
                execution_date=execution_date
            )
            db.session.add(order)
            db.session.commit()
            flash('Заказ успешно создан.', 'success')
            return redirect(url_for('index'))
        except ValueError:
            logger.error(f"Invalid quantity value: {quantity}")
            flash('Некорректное значение количества. Введите целое положительное число.', 'error')
            return redirect(url_for('order'))
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            flash(f'Ошибка при создании заказа: {str(e)}', 'error')
            return redirect(url_for('order'))

    try:
        partners = Partner.query.all()
        services = Service.query.all()
        return render_template('order.html', partners=partners, services=services)
    except Exception as e:
        logger.error(f"Error loading order page: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return render_template('order.html', partners=[], services=[])

# Форма добавления/редактирования партнера
@app.route('/partner/<int:partner_id>/edit', methods=['GET', 'POST'])
@app.route('/partner/new', methods=['GET', 'POST'])
def edit_partner(partner_id=None):
    partner_types = ['ИП', 'ООО', 'ЗАО']

    if request.method == 'POST':
        try:
            partner_name = request.form['partner_name']
            partner_type = request.form['partner_type']
            manager = request.form['manager']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            inn = request.form['inn']
            rating = request.form['rating']

            # Валидация данных
            if not all([partner_name, partner_type, manager, email, phone, address, inn, rating]):
                flash('Все поля обязательны для заполнения.', 'error')
                return redirect(request.url)

            if partner_type not in partner_types:
                flash('Недопустимый тип партнера. Выберите из списка.', 'error')
                return redirect(request.url)

            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                flash('Некорректный формат email.', 'error')
                return redirect(request.url)

            if not re.match(r'^\d{10,12}$', inn):
                flash('ИНН должен содержать 10 или 12 цифр.', 'error')
                return redirect(request.url)

            rating = int(rating)
            if rating < 0:
                flash('Рейтинг должен быть неотрицательным числом.', 'error')
                return redirect(request.url)

            if partner_id:
                partner = Partner.query.get_or_404(partner_id)
                if Partner.query.filter(Partner.partner_name == partner_name, Partner.partner_id != partner_id).first():
                    flash('Партнер с таким названием уже существует.', 'error')
                    return redirect(request.url)
                if Partner.query.filter(Partner.inn == inn, Partner.partner_id != partner_id).first():
                    flash('Партнер с таким ИНН уже существует.', 'error')
                    return redirect(request.url)
                partner.partner_name = partner_name
                partner.partner_type = partner_type
                partner.manager = manager
                partner.email = email
                partner.phone = phone
                partner.address = address
                partner.inn = inn
                partner.rating = rating
                action = 'отредактирован'
            else:
                if Partner.query.filter_by(partner_name=partner_name).first():
                    flash('Партнер с таким названием уже существует.', 'error')
                    return redirect(request.url)
                if Partner.query.filter_by(inn=inn).first():
                    flash('Партнер с таким ИНН уже существует.', 'error')
                    return redirect(request.url)
                partner = Partner(
                    partner_name=partner_name,
                    partner_type=partner_type,
                    manager=manager,
                    email=email,
                    phone=phone,
                    address=address,
                    inn=inn,
                    rating=rating
                )
                db.session.add(partner)
                action = 'добавлен'

            db.session.commit()
            flash(f'Партнер успешно {action}.', 'success')
            return redirect(url_for('index'))
        except ValueError:
            logger.error(f"Invalid rating value: {rating}")
            flash('Рейтинг должен быть целым неотрицательным числом.', 'error')
            return redirect(request.url)
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Integrity error for partner: {partner_name}, INN: {inn}")
            flash('Ошибка: Партнер с таким названием или ИНН уже существует.', 'error')
            return redirect(request.url)
        except Exception as e:
            logger.error(f"Error editing partner: {str(e)}")
            flash(f'Ошибка: {str(e)}', 'error')
            return redirect(request.url)

    try:
        partner = Partner.query.get(partner_id) if partner_id else None
        return render_template('edit_partner.html', partner=partner, partner_types=partner_types)
    except Exception as e:
        logger.error(f"Error loading edit partner page: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return render_template('edit_partner.html', partner=None, partner_types=partner_types)

# История услуг по партнеру
@app.route('/partner/<int:partner_id>/history')
def partner_history(partner_id):
    try:
        partner = Partner.query.get_or_404(partner_id)
        orders = Order.query.filter_by(partner_id=partner_id).join(Service).all()
        return render_template('partner_history.html', partner=partner, orders=orders)
    except Exception as e:
        logger.error(f"Error loading partner history for ID {partner_id}: {str(e)}")
        flash('Ошибка загрузки истории услуг.', 'error')
        return redirect(url_for('index'))

# Расчет себестоимости услуги
@app.route('/cost/<service_code>')
def cost(service_code):
    try:
        total_cost = calculate_service_cost(service_code)
        service = Service.query.filter_by(service_code=service_code).first()
        if not service:
            logger.error(f"Service not found: {service_code}")
            flash('Услуга не найдена.', 'error')
            return redirect(url_for('index'))
        service_name = service.service_name
        return render_template('cost.html', service_code=service_code, service_name=service_name, total_cost=total_cost)
    except Exception as e:
        logger.error(f"Error loading cost page for {service_code}: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return redirect(url_for('index'))

# Расчет количества материала
@app.route('/material', methods=['GET', 'POST'])
def material():
    if request.method == 'POST':
        try:
            service_type = request.form['service_type']
            material_type = request.form['material_type']
            quantity = int(request.form['quantity'])
            service_params = float(request.form['service_params'])

            # Валидация
            if quantity <= 0:
                flash('Количество должно быть положительным целым числом.', 'error')
                return redirect(url_for('material'))
            if service_params <= 0:
                flash('Параметры услуги должны быть положительным числом.', 'error')
                return redirect(url_for('material'))

            result = calculate_material_quantity(service_type, material_type, quantity, service_params)
            if result == -1:
                flash('Ошибка: неверный тип услуги или материала.', 'error')
                return redirect(url_for('material'))

            flash(f'Необходимое количество материала: {result} единиц.', 'success')
            return redirect(url_for('material'))
        except ValueError as e:
            logger.error(f"Invalid input for material calculation: {str(e)}")
            flash('Некорректные данные: количество должно быть целым, параметры услуги — числом.', 'error')
            return redirect(url_for('material'))
        except Exception as e:
            logger.error(f"Error in material calculation: {str(e)}")
            flash(f'Ошибка: {str(e)}', 'error')
            return redirect(url_for('material'))

    try:
        service_types = ServiceType.query.all()
        material_types = MaterialType.query.all()
        return render_template('material.html', service_types=service_types, material_types=material_types)
    except Exception as e:
        logger.error(f"Error loading material page: {str(e)}")
        flash('Ошибка загрузки страницы.', 'error')
        return render_template('material.html', service_types=[], material_types=[])

if __name__ == '__main__':
    app.run(debug=True)