create database banks_portal;
use banks_portal;
CREATE TABLE if not exists accounts (
    accountId int not null unique auto_increment,
    ownerName varchar(45) not null,
    owner_ssn int not null,
    balance decimal (10,2) default 0.00,
    account_status varchar(45)
    
);
ALTER TABLE accounts
ADD PRIMARY KEY (accountId);

CREATE TABLE Transactions (
    transactionId int not null unique auto_increment ,
    accountID int not null,
    transactionType varchar(45) not null,
    transactionAmount decimal (10,2) not null,
    primary key(transactionId)
  
);

INSERT INTO accounts (ownerName, owner_ssn, balance , account_status)
VALUES
 ('Maria Jozef', '123456789', '10000.00', 'active'),
 ("Linda Jones", "987654321", "2600.00", "inactive"),
 ("John McGrail", "222222222", "100.50", "active"),
 ("Patty luna", "111111111", "509.75", "inactive");

insert into Transactions ( accountID, transactionType, transactionAmount)
values
("1", "deposit", "650.98"),
("3", "withdraw", "899.87"),
("3", "deposit", "350.00");

DROP PROCEDURE IF EXISTS accountTransactions;

CREATE PROCEDURE accountTransactions(IN accountID INT)

SELECT * FROM accounts WHERE accountId = accountID;

drop procedure if exists deposit;


DELIMITER //

CREATE PROCEDURE deposit(IN accountID INT, IN amount DECIMAL(10,2))
BEGIN
   
INSERT INTO Transactions (accountID, transactionType, transactionAmount)
VALUES (accountID, 'deposit', amount);
UPDATE accounts SET balance = balance + amount WHERE accountId = accountID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE withdraw(IN accountID INT, IN amount DECIMAL(10,2))
BEGIN
INSERT INTO transactions (accountId, transactionType, transactionAmount)
VALUES (accountID, 'withdraw', amount);
UPDATE accounts SET balance = balance - amount WHERE accountId = accountID;
END //

DELIMITER ;




    




