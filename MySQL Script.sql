CREATE SCHEMA Business;

CREATE TABLE `Business`.`Customer` (
  `CustomerID` varchar(45) NOT NULL,
  `CustomerName` varchar(45) NOT NULL,
  `CustomerPassword` varchar(45) NOT NULL,
  `Gender` varchar(1) NOT NULL DEFAULT 'M',
  `EmailAddress` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `PhoneNumber` varchar(45) NOT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Administrator` (
  `AdministratorID` varchar(45) NOT NULL,
  `AdministratorName` varchar(45) NOT NULL,
  `AdministratorPassword` varchar(45) NOT NULL,
  `Gender` varchar(1)  NOT NULL DEFAULT 'M',
  `PhoneNumber` varchar(45) NOT NULL,
  PRIMARY KEY (`AdministratorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Products` (
  `ProductID` int NOT NULL,
  `Category` varchar(45) NOT NULL,
  `Model` varchar(45) NOT NULL,
  `Price` double NOT NULL,
  `Cost` double NOT NULL,
  `Warranty` double NOT NULL,
  `Inventory` double NOT NULL,
  PRIMARY KEY (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Items` (
  `ItemID` int NOT NULL,
  `PurchaseStatus` varchar(45) NOT NULL DEFAULT 'Unsold',
  `ServiceStatus` varchar(45) NOT NULL DEFAULT '',
  `ProductID` int NOT NULL,
  PRIMARY KEY (`ItemID`),
  FOREIGN KEY (`ProductID`) REFERENCES products(`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Purchased` (
  `CustomerID` varchar(45) NOT NULL,
  `ItemID` int NOT NULL,
  `PurchaseDate` datetime DEFAULT NULL,
  `WarrantyEndDate`  datetime DEFAULT NULL,
  PRIMARY KEY (`ItemID`),
  FOREIGN KEY (`CustomerID`) REFERENCES customer(`CustomerID`),
  FOREIGN KEY (`ItemID`) REFERENCES items(`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Request` (
  `RequestID` int NOT NULL AUTO_INCREMENT,
  `RequestDate` datetime DEFAULT NULL,
  `RequestStatus` varchar(45) NOT NULL,
  `CustomerID` varchar(45) NOT NULL,
  `ItemID` int NOT NULL,
  PRIMARY KEY (`RequestID`),
  FOREIGN KEY (`CustomerID`) REFERENCES customer(`CustomerID`),
  FOREIGN KEY (`ItemID`) REFERENCES items(`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`Service` (
  `ServiceID`int NOT NULL AUTO_INCREMENT,
  `ItemID` int NOT NULL,
  `RequestID` int NOT NULL,
  `AdministratorID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ServiceID`),
  FOREIGN KEY (`ItemID`) REFERENCES items(`ItemID`),
  FOREIGN KEY (`RequestID`) REFERENCES request(`RequestID`),
  FOREIGN KEY (`AdministratorID`) REFERENCES administrator(`AdministratorID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Business`.`ServiceFee` (
  `PaymentCreationDate` datetime DEFAULT NULL,
  `PaymentSettlementDate` datetime DEFAULT NULL,
  `DueDate` datetime DEFAULT NULL,
  `ServiceFeeAmount` double DEFAULT 0,
  `CustomerID` varchar(45) NOT NULL,
  `RequestID` int NOT NULL,
  PRIMARY KEY (`RequestID`),
  FOREIGN KEY (`CustomerID`) REFERENCES customer(`CustomerID`),
  FOREIGN KEY (`RequestID`) REFERENCES request(`RequestID`)
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;