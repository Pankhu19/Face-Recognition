create table user(
first_name char(30),
last_name char(30),
acc_no varchar(11) primary key,
mobile_no int(10),
email_id varchar(30),
pass varchar(30)
);
CREATE TABLE account (
  id INT(11) NOT NULL AUTO_INCREMENT,
  account_number varchar(11) NOT NULL,
  balance DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
  PRIMARY KEY (id),
  FOREIGN KEY (account_number) REFERENCES user(acc_no)
);
CREATE TABLE transaction (
  id INT(11) NOT NULL AUTO_INCREMENT,
  recep_name varchar(255) not null,
  recep_acc_no INT(11) NOT NULL,
  account_id INT(11) NOT NULL,
  transaction_type VARCHAR(255) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (account_id) REFERENCES account(id)
);
