-- Тестовые данные
INSERT INTO Users (Username, Email, Password, Role) VALUES
('admin', 'admin@example.com', '$2b$12$LPFOjG/6pb3teblH5vaQ4.3vw3tnEk4flCQ06vXBd9pzq06Og8622', 'manager'),
('analyst1', 'analyst@example.com', '$2b$12$erdv5nvXpdAFdhVBAhxe6uYJOJiZhKMNr5g1eSyOmHlgorsQBo.DW', 'analyst'),
('partner1', 'partner@example.com', '$2b$12$erdv5nvXpdAFdhVBAhxe6uYJOJiZhKMNr5g1eSyOmHlgorsQBo.DW', 'partner')
ON CONFLICT (Username) DO NOTHING;

INSERT INTO Partners (Name, LegalAddress, INN, DirectorFullName, Phone, Email, Rating) VALUES
('ООО "Паркет-Люкс"', 'г. Москва, ул. Лесная, д. 5', '772345678901', 'Иванов Сергей Петрович', '+7 (495) 111-22-33', 'info@parketlux.ru', 4.5),
('ИП Смирнов А.В.', 'г. Санкт-Петербург, Невский пр., д. 45', '781234567890', 'Смирнов Алексей Викторович', '+7 (812) 555-44-22', 'smirnov@flooring.spb.ru', 4.2),
('ООО "Пол-Мастер"', 'г. Казань, ул. Баумана, д. 10', '165432109876', 'Петров Иван Александрович', '+7 (843) 222-33-44', 'petrov@polmaster.ru', 4.0),
('ИП Кузнецов Д.В.', 'г. Новосибирск, ул. Горская, д. 15', '540123456789', 'Кузнецов Дмитрий Валерьевич', '+7 (383) 777-88-99', 'kuznetsov@flooring.ru', 3.8),
('ООО "Ламинат Про"', 'г. Екатеринбург, ул. Мира, д. 20', '667890123456', 'Сидоров Олег Николаевич', '+7 (343) 111-22-33', 'sidorov@laminatpro.ru', 4.3),
('ИП Васильев М.П.', 'г. Ростов-на-Дону, ул. Южная, д. 25', '616789012345', 'Васильев Михаил Павлович', '+7 (863) 444-55-66', 'vasiliev@floor.ru', 3.9),
('ООО "Полы России"', 'г. Самара, ул. Советская, д. 30', '631234567890', 'Морозов Андрей Сергеевич', '+7 (846) 666-77-88', 'morozov@polyrossii.ru', 4.1),
('ИП Лебедев В.А.', 'г. Уфа, ул. Центральная, д. 12', '027890123456', 'Лебедев Виктор Александрович', '+7 (347) 333-44-55', 'lebedev@flooring.uf.ru', 3.7),
('ООО "Эко Пол"', 'г. Краснодар, ул. Солнечная, д. 8', '231456789012', 'Ковалёв Павел Игоревич', '+7 (861) 555-66-77', 'kovalev@ecopol.ru', 4.4),
('ИП Григорьев С.Н.', 'г. Челябинск, ул. Металлургов, д. 17', '745678901234', 'Григорьев Сергей Николаевич', '+7 (351) 222-33-44', 'grigoryev@flooring.chl.ru', 3.6),
('ООО "Паркетный Дом"', 'г. Владивосток, ул. Морская, д. 9', '253456789012', 'Фёдоров Игорь Васильевич', '+7 (423) 777-88-99', 'fedorov@parketdom.ru', 4.0),
('ИП Зайцев А.В.', 'г. Калининград, ул. Балтийская, д. 14', '391234567890', 'Зайцев Антон Викторович', '+7 (401) 444-55-66', 'zaytsev@flooring.kal.ru', 3.8),
('ООО "Полы Сибири"', 'г. Омск, ул. Ленина, д. 22', '550123456789', 'Николаев Сергей Михайлович', '+7 (381) 666-77-88', 'nikolaev@polysibiri.ru', 4.2),
('ИП Соколов Д.А.', 'г. Пермь, ул. Комсомольская, д. 11', '590123456789', 'Соколов Дмитрий Александрович', '+7 (342) 333-44-55', 'sokolov@flooring.perm.ru', 3.9),
('ООО "Линолеум Про"', 'г. Волгоград, ул. Мира, д. 19', '344567890123', 'Козлов Олег Петрович', '+7 (844) 555-66-77', 'kozlov@linoleumpro.ru', 4.1),
('ИП Беляев М.В.', 'г. Саратов, ул. Советская, д. 23', '645678901234', 'Беляев Максим Викторович', '+7 (845) 222-33-44', 'belyaev@flooring.sar.ru', 3.7),
('ООО "Ковролин"', 'г. Нижний Новгород, ул. Горького, д. 15', '526789012345', 'Михайлов Андрей Игоревич', '+7 (831) 777-88-99', 'mikhailov@kovrolin.ru', 4.0),
('ИП Гусев С.В.', 'г. Воронеж, пр. Революции, д. 56', '366789012345', 'Гусев Сергей Владимирович', '+7 (473) 555-88-00', 'gusev@floorstore.ru', 3.7)
ON CONFLICT (Name) DO NOTHING;

INSERT INTO Managers (FullName, Phone, Email) VALUES
('Иванов Алексей Сергеевич', '+7 (495) 123-45-67', 'ivanov@masterpol.ru'),
('Петрова Ольга Викторовна', '+7 (495) 234-56-78', 'petrova@masterpol.ru'),
('Сидоров Игорь Михайлович', '+7 (495) 345-67-89', 'sidorov@masterpol.ru')
ON CONFLICT (Email) DO NOTHING;

INSERT INTO Suppliers (Name, INN, Phone, Email) VALUES
('ООО "Материал-Снаб"', '123456789012', '+7 (495) 678-90-12', 'snab@material.ru'),
('ИП Ковалёв П.В.', '987654321098', '+7 (495) 789-01-23', 'kovalev@supply.ru')
ON CONFLICT (Name) DO NOTHING;

INSERT INTO Materials (Name, Unit, Cost, QuantityInStock, MinAllowedQuantity) VALUES
('Ламинат', 'м²', 1200.00, 500.00, 50.00),
('Паркетная доска', 'м²', 2500.00, 300.00, 30.00),
('Клей для паркета', 'л', 500.00, 200.00, 20.00)
ON CONFLICT (Name) DO NOTHING;

INSERT INTO Supplies (SupplierID, MaterialID, ManagerID, Quantity, SupplyDate) VALUES
(1, 1, 1, 100.00, '2025-10-01 10:00:00'),
(2, 2, 2, 50.00, '2025-10-02 12:00:00')
ON CONFLICT DO NOTHING;

INSERT INTO Products (Name, Description, StandardNumber, ManufactureTimeDays, CostPrice, MinPartnerPrice) VALUES
('Ламинат "Дуб"', 'Ламинат высокого качества', 'ST-123', 5, 1000.00, 1200.00),
('Паркет "Ясень"', 'Паркет натуральный', 'ST-456', 7, 2000.00, 2400.00)
ON CONFLICT (Name) DO NOTHING;

INSERT INTO ProductComposition (ProductID, MaterialID, Quantity) VALUES
(1, 1, 1.00),
(2, 2, 1.00),
(2, 3, 0.10)
ON CONFLICT DO NOTHING;

INSERT INTO Requests (PartnerID, ManagerID, ProductID, Quantity, UnitPrice, Status) VALUES
(1, 1, 1, 50, 1300.00, 'Новая'),
(2, 2, 2, 30, 2500.00, 'Выполнена')
ON CONFLICT DO NOTHING;

-- Добавляем партнёра
INSERT INTO Partners (PartnerID, Name, INN) VALUES (1, 'ООО СтройМат', '123456789012') ON CONFLICT DO NOTHING;

-- Добавляем менеджера
INSERT INTO Managers (ManagerID, FullName) VALUES (1, 'Петров Иван Александрович') ON CONFLICT DO NOTHING;

-- Добавляем продукт
INSERT INTO Products (ProductID, Name, MinPartnerPrice) VALUES (1, 'Паркетная доска', 1300.00) ON CONFLICT DO NOTHING;

-- Добавляем пользователя-партнёра
INSERT INTO Users (Username, Email, Password, Role, PartnerID) 
VALUES ('partner1', 'partner@example.com', '$2b$12$hashed_password', 'partner', 1) ON CONFLICT DO NOTHING;

-- Добавляем пользователя-менеджера
INSERT INTO Users (Username, Email, Password, Role) 
VALUES ('manager1', 'manager@example.com', '$2b$12$hashed_password', 'manager') ON CONFLICT DO NOTHING;

-- Добавляем выполненную заявку для партнёра
INSERT INTO Requests (PartnerID, ManagerID, ProductID, Quantity, UnitPrice, Status) 
VALUES (1, 1, 1, 10, 1500.00, 'Выполнена') ON CONFLICT DO NOTHING;

-- Проверяем данные
SELECT * FROM Requests WHERE PartnerID = 1 AND Status = 'Выполнена';

-- Привязываем aboba123 к PartnerID=3
UPDATE Users SET PartnerID = 3 WHERE UserID = 6 AND Username = 'aboba123';

-- Проверяем обновление
SELECT * FROM Users WHERE Username = 'aboba123';

-- Добавляем продукт (если ещё не добавлен)
INSERT INTO Products (ProductID, Name, MinPartnerPrice)
VALUES (1, 'Паркетная доска', 1300.00)
ON CONFLICT (ProductID) DO NOTHING;

-- Добавляем менеджера (если ещё не добавлен)
INSERT INTO Managers (ManagerID, FullName)
VALUES (1, 'Петров Иван Александрович')
ON CONFLICT (ManagerID) DO NOTHING;

-- Добавляем выполненную заявку для PartnerID=3
INSERT INTO Requests (RequestID, PartnerID, ManagerID, ProductID, Quantity, UnitPrice, Status, CreatedAt)
VALUES (3, 3, 1, 1, 10, 1500.00, 'Выполнена', '2025-10-22 10:04:06.914423')
ON CONFLICT (RequestID) DO NOTHING;

-- Проверяем заявку
SELECT * FROM Requests WHERE PartnerID = 3 AND Status = 'Выполнена';

