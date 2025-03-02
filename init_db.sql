DROP TABLE IF EXISTS COMPANY;

CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) VALUES
(1, 'Solvd Inc.', 10, '39a Mahiliouskaya str. apt 401, Minsk', 200.0),
(2, 'ISSoft', 20, '5 Chapayeva str, Minsk', 500.0),
(3, 'Grid Dynamics Inc.', 20, '78 Grzybowska str, Warszawa', 600.0);