CREATE DATABASE MediTrackPro;
USE MediTrackPro;
--DDL(Data Definition Language)
-- Patient Table
CREATE TABLE Patient (
    PatientID   INT PRIMARY KEY,
    FirstName   VARCHAR(50),
    LastName    VARCHAR(50),
    DOB         DATE,
    Gender      VARCHAR(10),
    Phone       VARCHAR(15),
    Address     VARCHAR(200),
    BloodGroup  VARCHAR(5)
);

-- Doctor Table
CREATE TABLE Doctor (
    DoctorID       INT PRIMARY KEY,
    FirstName      VARCHAR(50),
    LastName       VARCHAR(50),
    Specialization VARCHAR(100),
    LicenseNo      VARCHAR(30),
    Phone          VARCHAR(15)
);

-- Medicine Table
CREATE TABLE Medicine (
    MedicineID    INT PRIMARY KEY,
    MedicineName  VARCHAR(100),
    Category      VARCHAR(50),
    DosageForm    VARCHAR(50),
    UnitPrice     DECIMAL(10,2),
    StockQty      INT,
    ExpiryDate    DATE,
    ReorderLevel  INT
);

-- Supplier Table
CREATE TABLE Supplier (
    SupplierID    INT PRIMARY KEY,
    SupplierName  VARCHAR(100),
    ContactPerson VARCHAR(100),
    Phone         VARCHAR(15),
    Address       VARCHAR(200)
);

-- Prescription Table
CREATE TABLE Prescription (
    PrescriptionID   INT PRIMARY KEY,
    PatientID        INT FOREIGN KEY REFERENCES Patient(PatientID),
    DoctorID         INT FOREIGN KEY REFERENCES Doctor(DoctorID),
    PrescriptionDate DATE,
    Diagnosis        VARCHAR(200),
    Status           VARCHAR(20)
);

-- Prescription Item Table
CREATE TABLE Prescription_Item (
    ItemID         INT PRIMARY KEY,
    PrescriptionID INT FOREIGN KEY REFERENCES Prescription(PrescriptionID),
    MedicineID     INT FOREIGN KEY REFERENCES Medicine(MedicineID),
    Quantity       INT,
    Dosage         VARCHAR(50),
    Frequency      VARCHAR(50),
    DurationDays   INT
);

-- Inventory Log Table
CREATE TABLE Inventory_Log (
    LogID           INT PRIMARY KEY,
    MedicineID      INT FOREIGN KEY REFERENCES Medicine(MedicineID),
    TransactionType VARCHAR(20),
    Quantity        INT,
    LogDate         DATE,
    Notes           VARCHAR(200)
);

-- Supply Order Table
CREATE TABLE Supply_Order (
    OrderID         INT PRIMARY KEY,
    SupplierID      INT FOREIGN KEY REFERENCES Supplier(SupplierID),
    MedicineID      INT FOREIGN KEY REFERENCES Medicine(MedicineID),
    OrderedQty      INT,
    UnitPrice       DECIMAL(10,2),
    OrderDate       DATE,
    Status          VARCHAR(20)
);

--DML (Data Manipulation Language)
-- Insert Patients
INSERT INTO Patient VALUES (1, 'Ali', 'Hassan', '1990-05-12', 'Male', '03001234567', 'Lahore', 'B+');
INSERT INTO Patient VALUES (2, 'Sara', 'Khan', '1985-08-22', 'Female', '03109876543', 'Karachi', 'A+');
INSERT INTO Patient VALUES (3, 'Umar', 'Farooq', '2000-01-30', 'Male', '03321122334', 'Islamabad', 'O-');
INSERT INTO Patient VALUES (4, 'Hira', 'Malik', '1995-03-18', 'Female', '03451234567', 'Peshawar', 'A-');
INSERT INTO Patient VALUES (5, 'Bilal', 'Ahmed', '1988-11-05', 'Male', '03561234567', 'Multan', 'O+');

-- Insert Doctors
INSERT INTO Doctor VALUES (1, 'Ayesha', 'Malik', 'Cardiologist', 'LIC-001', '03001111111');
INSERT INTO Doctor VALUES (2, 'Bilal', 'Chaudhry', 'General Physician', 'LIC-002', '03002222222');
INSERT INTO Doctor VALUES (3, 'Sana', 'Rizvi', 'Diabetologist', 'LIC-003', '03003333333');

-- Insert Medicines
INSERT INTO Medicine VALUES (1, 'Paracetamol 500mg', 'Analgesic', 'Tablet', 5.00, 500, '2026-12-31', 100);
INSERT INTO Medicine VALUES (2, 'Amoxicillin 250mg', 'Antibiotic', 'Capsule', 25.00, 300, '2025-09-30', 50);
INSERT INTO Medicine VALUES (3, 'Metformin 500mg', 'Antidiabetic', 'Tablet', 12.00, 400, '2027-03-31', 80);
INSERT INTO Medicine VALUES (4, 'Omeprazole 20mg', 'Antacid', 'Capsule', 18.00, 250, '2026-06-30', 60);
INSERT INTO Medicine VALUES (5, 'Atorvastatin 10mg', 'Statin', 'Tablet', 30.00, 45, '2026-11-30', 40);
INSERT INTO Medicine VALUES (6, 'Cetirizine 10mg', 'Antihistamine', 'Tablet', 8.00, 600, '2027-01-31', 70);

-- Insert Suppliers
INSERT INTO Supplier VALUES (1, 'MedPlus Distributors', 'Tariq Ahmed', '042-35123456', 'Model Town, Lahore');
INSERT INTO Supplier VALUES (2, 'PharmaCo Supplies', 'Nadia Iqbal', '021-34567890', 'Clifton, Karachi');

-- Insert Prescriptions
INSERT INTO Prescription VALUES (1, 1, 1, '2026-04-10', 'Viral Fever', 'Dispensed');
INSERT INTO Prescription VALUES (2, 2, 3, '2026-04-11', 'Type 2 Diabetes', 'Pending');
INSERT INTO Prescription VALUES (3, 3, 2, '2026-04-12', 'Common Cold', 'Dispensed');
INSERT INTO Prescription VALUES (4, 4, 1, '2026-04-13', 'Hypertension', 'Pending');
INSERT INTO Prescription VALUES (5, 5, 2, '2026-04-14', 'Acid Reflux', 'Dispensed');

-- Insert Prescription Items
INSERT INTO Prescription_Item VALUES (1, 1, 1, 10, '500mg', 'Twice daily', 5);
INSERT INTO Prescription_Item VALUES (2, 1, 2, 14, '250mg', 'Three times daily', 7);
INSERT INTO Prescription_Item VALUES (3, 2, 3, 30, '500mg', 'Once daily', 30);
INSERT INTO Prescription_Item VALUES (4, 2, 4, 30, '20mg', 'Once daily', 30);
INSERT INTO Prescription_Item VALUES (5, 3, 1, 6, '500mg', 'Three times daily', 2);
INSERT INTO Prescription_Item VALUES (6, 3, 6, 5, '10mg', 'Once daily', 5);
INSERT INTO Prescription_Item VALUES (7, 5, 4, 14, '20mg', 'Twice daily', 7);

-- Insert Inventory Logs
INSERT INTO Inventory_Log VALUES (1, 1, 'Restock', 200, '2026-04-01', 'Opening stock');
INSERT INTO Inventory_Log VALUES (2, 2, 'Restock', 300, '2026-04-01', 'Opening stock');
INSERT INTO Inventory_Log VALUES (3, 1, 'Dispensed', 16, '2026-04-10', 'Given to patient Ali');
INSERT INTO Inventory_Log VALUES (4, 5, 'Damaged', 10, '2026-04-05', 'Packaging broken');

-- Insert Supply Orders
INSERT INTO Supply_Order VALUES (1, 1, 1, 500, 4.00, '2026-04-01', 'Received');
INSERT INTO Supply_Order VALUES (2, 2, 3, 300, 11.00, '2026-04-10', 'Ordered');
INSERT INTO Supply_Order VALUES (3, 1, 5, 200, 28.00, '2026-04-12', 'Ordered');

--UPDATE
-- Update patient phone number
UPDATE Patient
SET Phone = '03009999999'
WHERE PatientID = 1;

-- Update medicine price
UPDATE Medicine
SET UnitPrice = 27.00
WHERE MedicineID = 2;

-- Update prescription status
UPDATE Prescription
SET Status = 'Dispensed'
WHERE PrescriptionID = 2;

-- Update stock quantity after restock
UPDATE Medicine
SET StockQty = StockQty + 200
WHERE MedicineID = 5;

--DELETE
-- Delete a supply order
DELETE FROM Supply_Order
WHERE OrderID = 3;

-- Delete an inventory log entry
DELETE FROM Inventory_Log
WHERE LogID = 4;

--SELECT
-- View all patients
SELECT * FROM Patient;

-- View all medicines
SELECT * FROM Medicine;

-- View all pending prescriptions
SELECT * FROM Prescription
WHERE Status = 'Pending';

-- View prescriptions with patient names
SELECT Prescription.PrescriptionID, Patient.FirstName, Patient.LastName,
       Prescription.Diagnosis, Prescription.Status
FROM Prescription, Patient
WHERE Prescription.PatientID = Patient.PatientID;

-- View medicines that are low in stock
SELECT MedicineName, StockQty, ReorderLevel
FROM Medicine
WHERE StockQty < ReorderLevel;

-- Aggregate Functions

-- COUNT: How many patients are registered
SELECT COUNT(*) AS TotalPatients
FROM Patient;

-- COUNT: How many prescriptions each doctor has written
SELECT DoctorID, COUNT(*) AS TotalPrescriptions
FROM Prescription
GROUP BY DoctorID;

-- SUM: Total stock quantity of all medicines
SELECT SUM(StockQty) AS TotalStock
FROM Medicine;

-- SUM: Total value of all medicine stock
SELECT SUM(StockQty * UnitPrice) AS TotalInventoryValue
FROM Medicine;

-- AVG: Average price of all medicines
SELECT AVG(UnitPrice) AS AveragePrice
FROM Medicine;

-- AVG: Average price by category
SELECT Category, AVG(UnitPrice) AS AvgPrice
FROM Medicine
GROUP BY Category;

-- MAX: Most expensive medicine
SELECT MAX(UnitPrice) AS MaxPrice
FROM Medicine;

-- MIN: Cheapest medicine
SELECT MIN(UnitPrice) AS MinPrice
FROM Medicine;

-- COUNT with HAVING: Categories with more than 1 medicine
SELECT Category, COUNT(*) AS TotalMedicines
FROM Medicine
GROUP BY Category
HAVING COUNT(*) > 1;

-- SUM: Total quantity prescribed per medicine
SELECT MedicineID, SUM(Quantity) AS TotalPrescribed
FROM Prescription_Item
GROUP BY MedicineID;

--User Defined Functions

-- -----------------------------------------------
-- UDF 1 (Scalar): Get patient full name by ID
-- -----------------------------------------------
CREATE FUNCTION fn_PatientName (@PatientID INT)
RETURNS VARCHAR(100)
AS
BEGIN
    DECLARE @Name VARCHAR(100);
    SELECT @Name = FirstName + ' ' + LastName
    FROM Patient
    WHERE PatientID = @PatientID;
    RETURN @Name;
END;

-- Usage:
SELECT dbo.fn_PatientName(1) AS PatientName;


-- -----------------------------------------------
-- UDF 2 (Scalar): Calculate total cost of a prescription
-- -----------------------------------------------
CREATE FUNCTION fn_PrescriptionCost (@PrescriptionID INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Cost DECIMAL(10,2);
    SELECT @Cost = SUM(pi.Quantity * m.UnitPrice)
    FROM Prescription_Item pi, Medicine m
    WHERE pi.MedicineID = m.MedicineID
    AND pi.PrescriptionID = @PrescriptionID;
    RETURN @Cost;
END;

-- Usage:
SELECT dbo.fn_PrescriptionCost(1) AS TotalCost;


-- -----------------------------------------------
-- UDF 3 (Scalar): Check if a medicine is low in stock
-- -----------------------------------------------
CREATE FUNCTION fn_StockStatus (@MedicineID INT)
RETURNS VARCHAR(20)
AS
BEGIN
    DECLARE @Qty INT;
    DECLARE @Reorder INT;
    DECLARE @Status VARCHAR(20);

    SELECT @Qty = StockQty, @Reorder = ReorderLevel
    FROM Medicine
    WHERE MedicineID = @MedicineID;

    IF @Qty = 0
        SET @Status = 'Out of Stock';
    ELSE IF @Qty < @Reorder
        SET @Status = 'Low Stock';
    ELSE
        SET @Status = 'Available';

    RETURN @Status;
END;

-- Usage:
SELECT MedicineName, dbo.fn_StockStatus(MedicineID) AS StockStatus
FROM Medicine;


-- -----------------------------------------------
-- UDF 4 (Table-Valued): Get all prescriptions of a patient
-- -----------------------------------------------
CREATE FUNCTION fn_PatientPrescriptions (@PatientID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT PrescriptionID, PrescriptionDate, Diagnosis, Status
    FROM Prescription
    WHERE PatientID = @PatientID
);

-- Usage:
SELECT * FROM dbo.fn_PatientPrescriptions(2);


-- -----------------------------------------------
-- UDF 5 (Table-Valued): Get all medicines below reorder level
-- -----------------------------------------------
CREATE FUNCTION fn_LowStockMedicines (@Threshold INT)
RETURNS TABLE
AS
RETURN
(
    SELECT MedicineName, Category, StockQty, ReorderLevel
    FROM Medicine
    WHERE StockQty < @Threshold
);

-- Usage:
SELECT * FROM dbo.fn_LowStockMedicines(100);

--phase 3
--Views
CREATE VIEW vw_ActivePrescriptions
AS
SELECT
    Prescription.PrescriptionID,
    Patient.FirstName + ' ' + Patient.LastName AS PatientName,
    Doctor.FirstName + ' ' + Doctor.LastName AS DoctorName,
    Prescription.PrescriptionDate,
    Prescription.Diagnosis,
    Prescription.Status
FROM Prescription, Patient, Doctor
WHERE Prescription.PatientID = Patient.PatientID
AND Prescription.DoctorID = Doctor.DoctorID
AND Prescription.Status = 'Pending';

-- Use the view
SELECT * FROM vw_ActivePrescriptions;

CREATE VIEW vw_MedicineStock
AS
SELECT
    MedicineID,
    MedicineName,
    Category,
    StockQty,
    ReorderLevel,
    CASE
        WHEN StockQty = 0 THEN 'Out of Stock'
        WHEN StockQty < ReorderLevel THEN 'Low Stock'
        ELSE 'Available'
    END AS StockStatus
FROM Medicine;

-- Use the view
SELECT * FROM vw_MedicineStock;

CREATE VIEW vw_PrescriptionItems
AS
SELECT
    Prescription.PrescriptionID,
    Patient.FirstName + ' ' + Patient.LastName AS PatientName,
    Prescription.Diagnosis,
    Medicine.MedicineName,
    Prescription_Item.Quantity,
    Prescription_Item.Dosage,
    Prescription_Item.Frequency,
    Prescription_Item.DurationDays
FROM Prescription, Patient, Prescription_Item, Medicine
WHERE Prescription.PatientID = Patient.PatientID
AND Prescription_Item.PrescriptionID = Prescription.PrescriptionID
AND Prescription_Item.MedicineID = Medicine.MedicineID;

-- Use the view
SELECT * FROM vw_PrescriptionItems;

-- See items of one specific prescription
SELECT * FROM vw_PrescriptionItems
WHERE PrescriptionID = 1;


CREATE VIEW vw_SupplierOrders
AS
SELECT
    Supply_Order.OrderID,
    Supplier.SupplierName,
    Medicine.MedicineName,
    Supply_Order.OrderedQty,
    Supply_Order.UnitPrice,
    Supply_Order.OrderDate,
    Supply_Order.Status
FROM Supply_Order, Supplier, Medicine
WHERE Supply_Order.SupplierID = Supplier.SupplierID
AND Supply_Order.MedicineID = Medicine.MedicineID;

-- Use the view
SELECT * FROM vw_SupplierOrders;


CREATE VIEW vw_PatientList
AS
SELECT
    PatientID,
    FirstName + ' ' + LastName AS FullName,
    Gender,
    Phone,
    BloodGroup
FROM Patient;

-- Use the view
SELECT * FROM vw_PatientList;


-- Stored Procedures

CREATE PROCEDURE sp_AddNewPatient
    @PatientID  INT,
    @FirstName  VARCHAR(50),
    @LastName   VARCHAR(50),
    @DOB        DATE,
    @Gender     VARCHAR(10),
    @Phone      VARCHAR(15),
    @Address    VARCHAR(200),
    @BloodGroup VARCHAR(5)
AS
BEGIN
    INSERT INTO Patient
    VALUES (@PatientID, @FirstName, @LastName,
            @DOB, @Gender, @Phone, @Address, @BloodGroup);

    PRINT 'Patient added successfully.';
END;

-- Call the procedure
EXEC sp_AddNewPatient 6, 'Zara', 'Hussain', '1998-07-15',
     'Female', '03701234567', 'Faisalabad', 'AB+';

-- Check the result
SELECT * FROM Patient;


CREATE PROCEDURE sp_AddNewMedicine
    @MedicineID   INT,
    @MedicineName VARCHAR(100),
    @Category     VARCHAR(50),
    @DosageForm   VARCHAR(50),
    @UnitPrice    DECIMAL(10,2),
    @StockQty     INT,
    @ExpiryDate   DATE,
    @ReorderLevel INT
AS
BEGIN
    INSERT INTO Medicine
    VALUES (@MedicineID, @MedicineName, @Category,
            @DosageForm, @UnitPrice, @StockQty,
            @ExpiryDate, @ReorderLevel);

    PRINT 'Medicine added successfully.';
END;

-- Call the procedure
EXEC sp_AddNewMedicine 7, 'Ibuprofen 400mg', 'Analgesic',
     'Tablet', 15.00, 350, '2027-06-30', 60;

-- Check the result
SELECT * FROM Medicine;


CREATE PROCEDURE sp_RestockMedicine
    @MedicineID INT,
    @Quantity   INT,
    @Notes      VARCHAR(200)
AS
BEGIN
    -- Add stock to medicine
    UPDATE Medicine
    SET StockQty = StockQty + @Quantity
    WHERE MedicineID = @MedicineID;

    -- Record in log
    INSERT INTO Inventory_Log
    VALUES (
        (SELECT MAX(LogID) + 1 FROM Inventory_Log),
        @MedicineID,
        'Restock',
        @Quantity,
        GETDATE(),
        @Notes
    );

    PRINT 'Stock updated successfully.';
END;

-- Call the procedure
EXEC sp_RestockMedicine 5, 150, 'Received from MedPlus April 2025';

-- Check the result
SELECT MedicineID, MedicineName, StockQty
FROM Medicine WHERE MedicineID = 5;

SELECT * FROM Inventory_Log WHERE MedicineID = 5;



CREATE PROCEDURE sp_GetPatientPrescriptions
    @PatientID INT
AS
BEGIN
    SELECT
        Prescription.PrescriptionID,
        Prescription.PrescriptionDate,
        Prescription.Diagnosis,
        Prescription.Status,
        Medicine.MedicineName,
        Prescription_Item.Dosage,
        Prescription_Item.Frequency,
        Prescription_Item.DurationDays
    FROM Prescription, Prescription_Item, Medicine
    WHERE Prescription.PrescriptionID = Prescription_Item.PrescriptionID
    AND Prescription_Item.MedicineID = Medicine.MedicineID
    AND Prescription.PatientID = @PatientID;
END;

-- Call the procedure
EXEC sp_GetPatientPrescriptions 1;
EXEC sp_GetPatientPrescriptions 2;



CREATE PROCEDURE sp_UpdatePrescriptionStatus
    @PrescriptionID INT,
    @NewStatus      VARCHAR(20)
AS
BEGIN
    UPDATE Prescription
    SET Status = @NewStatus
    WHERE PrescriptionID = @PrescriptionID;

    PRINT 'Prescription status updated successfully.';
END;

-- Call the procedure
EXEC sp_UpdatePrescriptionStatus 2, 'Dispensed';
EXEC sp_UpdatePrescriptionStatus 4, 'Expired';

-- Check the result
SELECT PrescriptionID, Diagnosis, Status FROM Prescription;



CREATE TRIGGER trg_PreventNegativeStock
ON Medicine
AFTER UPDATE
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE StockQty < 0)
    BEGIN
        RAISERROR ('Error: Stock cannot be less than zero.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;

-- Test: this update should be blocked by the trigger
UPDATE Medicine
SET StockQty = -5
WHERE MedicineID = 1;

-- Check that stock was NOT changed
SELECT MedicineID, MedicineName, StockQty
FROM Medicine WHERE MedicineID = 1;



CREATE TRIGGER trg_LogStockUpdate
ON Medicine
AFTER UPDATE
AS
BEGIN
    IF UPDATE(StockQty)
    BEGIN
        INSERT INTO Inventory_Log
        VALUES (
            (SELECT MAX(LogID) + 1 FROM Inventory_Log),
            (SELECT MedicineID FROM inserted),
            'Restock',
            (SELECT StockQty FROM inserted) -
            (SELECT StockQty FROM deleted),
            GETDATE(),
            'Stock was updated automatically'
        );
    END
END;

-- Test: update stock and see if log is created
UPDATE Medicine
SET StockQty = StockQty + 100
WHERE MedicineID = 2;

-- Check the automatic log entry
SELECT * FROM Inventory_Log ORDER BY LogID DESC;



CREATE TRIGGER trg_BlockDeletePatient
ON Patient
INSTEAD OF DELETE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM Prescription
        WHERE PatientID IN (SELECT PatientID FROM deleted)
    )
    BEGIN
        PRINT 'Cannot delete patient. This patient has prescriptions in the system.';
    END
    ELSE
    BEGIN
        DELETE FROM Patient
        WHERE PatientID IN (SELECT PatientID FROM deleted);
        PRINT 'Patient deleted successfully.';
    END
END;

-- Test 1: Try to delete a patient who has prescriptions (should be blocked)
DELETE FROM Patient WHERE PatientID = 1;

-- Test 2: Try to delete patient 6 who was just added and has no prescriptions
DELETE FROM Patient WHERE PatientID = 6;

-- Check the result
SELECT * FROM Patient;



CREATE TRIGGER trg_AutoLogSupplyOrder
ON Supply_Order
AFTER INSERT
AS
BEGIN
    INSERT INTO Inventory_Log
    VALUES (
        (SELECT MAX(LogID) + 1 FROM Inventory_Log),
        (SELECT MedicineID FROM inserted),
        'Restock',
        (SELECT OrderedQty FROM inserted),
        GETDATE(),
        'New supply order placed'
    );

    PRINT 'Inventory log updated for new supply order.';
END;

-- Test: add a new supply order
INSERT INTO Supply_Order
VALUES (4, 1, 2, 400, 22.00, '2025-04-20', 'Ordered');

-- Check the automatic log entry
SELECT * FROM Inventory_Log ORDER BY LogID DESC;



--Indexes
CREATE INDEX idx_Patient_Phone
ON Patient (Phone);

-- Test it
SELECT * FROM Patient
WHERE Phone = '03001234567';


CREATE INDEX idx_Medicine_Category
ON Medicine (Category);

-- Test it
SELECT * FROM Medicine
WHERE Category = 'Analgesic';


CREATE INDEX idx_Prescription_Status
ON Prescription (Status);

-- Test it
SELECT * FROM Prescription
WHERE Status = 'Pending';



CREATE INDEX idx_Prescription_PatientID
ON Prescription (PatientID);

-- Test it
SELECT * FROM Prescription
WHERE PatientID = 2;


CREATE INDEX idx_Medicine_ExpiryDate
ON Medicine (ExpiryDate);

-- Test it
SELECT MedicineName, ExpiryDate, StockQty
FROM Medicine
WHERE ExpiryDate < '2027-01-01'
ORDER BY ExpiryDate ASC;



CREATE INDEX idx_InventoryLog_MedicineID
ON Inventory_Log (MedicineID);

-- Test it
SELECT * FROM Inventory_Log
WHERE MedicineID = 1;