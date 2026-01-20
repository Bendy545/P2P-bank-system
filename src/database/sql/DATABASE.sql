-- ============================================================
-- Project: P2P Bank System
-- Author: Martin Chmelík
-- Email: jchmelikmartin123@gmail.com
-- ============================================================

START TRANSACTION;

create database p2p_bank;

use p2p_bank;

create table accounts(
id int primary key auto_increment,
account_no int not null check(account_no between 10000 and 99999),
bank_code varchar(15) not null,
balance bigint unsigned not null default 0 check(balance >= 0),
created_at timestamp default current_timestamp not null,
updated_at timestamp default current_timestamp not null on update current_timestamp,

unique key uq_accounts_bank_account (bank_code, account_no)
);

create index ix_accounts_bank_code on accounts(bank_code);

create table account_tx(
id int primary key auto_increment,
account_id int not null,
tx_type char(1) not null check(tx_type in ('D', 'W')),
amount bigint unsigned not null check(amount >= 0),
created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

foreign key(account_id) references accounts(id) on delete cascade
);

create table node_log(
id int primary key auto_increment,
created_at timestamp not null default current_timestamp,
level_name varchar(40) not null default 'INFO' check(level_name in ('INFO', 'WARN', 'ERROR', 'DEBUG')),
event_type varchar(50) not null,
client_ip varchar(45),
client_port int,
command char(2),
account_no int check(account_no between 10000 and 99999),
bank_code varchar(15),
request_raw varchar(1000),
response_raw varchar(1000),
message varchar(1000) not null
);

commit;