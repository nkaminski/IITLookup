CREATE TABLE iitlookup ( first_name VARCHAR(32), middle_name VARCHAR(32), last_name VARCHAR(32), idnumber VARCHAR(9) NOT NULL, card_number INTEGER, PRIMARY KEY(idnumber), INDEX(card_number));
