INSERT INTO staff VALUES
('11', 'D', 'Doc A', '6f1b5f5df5d7d4fc92f1544b22927f6a3b6f9ea34588f235940ad93f', 'b9f2543b33a3adfd08e21a1f0213208ba77be211b7e1c212e0cb37fa'),
('12', 'D', 'Doc B', '28b41edf3b0dd7a48604f73ecb5fe2a456c58395faf0d1fae774b92b', '6024a299a4467214e4d29724f3a50d75deb967d7105141158cb1a8e0'),
('21', 'N', 'Nurse A', 'd8b1a785f215fd87747f37b1be12da2e841ce1ecb9a40b0e8db71dd1', '0f03f04c16c1651710f29feda3d02413867675cd0745ba4c6c16b299'),
('22', 'N', 'Nurse B', 'dc04aeaf8728f57fb389ac3d2f814a8d78d101cb39b4b15b617955f6', '941607c42e98281008a92ef771d26d97db7533e81c2c98516086724d'),
('31', 'A', 'Admin A', '9fa38f2c81f142f881c5a9d0d8c462fbb3d2b2c93123bf4438baf3d2', '2bdf983dc86f4159188b03f40698b0624bb76070df3ba727ad26e7ac'),
('32', 'A', 'Admin B', '9b590109635183644227f5f2bffac2f5e864c49863c1df1a839cd2b3', '62a764eb5e88b83bce26baf3d09159c5d5a69e51afed3dc9adb8838b');

INSERT INTO patients VALUES
('1', 'Ed A', 'kid', '123 Edmonton', '1234567890', '0987654321'),
('2', 'Ed B', 'kid', '456 Calgary', '2345678901', '1098765432'),
('3', 'Ed C', 'adult', '789 Toronto', '3456789012', '2109876543'),
('4', 'Ed D', 'adult', '420 Vancouver', '4567890123', '3210987654'),
('5', 'Ed E', 'elder', '808 Montreal', '5678901234', '4321098765'),
('6', 'Ed F', 'elder', '666 Phoenix', '1313131313', '6666666666');


INSERT INTO charts VALUES
('11', '1', '2010-01-02', '2011-03-04'),
('12', '1', '2016-01-27', NULL),
('21', '2', '2013-12-31', '2014-07-07'),
('31', '3', '2016-07-11', NULL),
('41', '4', '2015-05-30', '2015-06-07'),
('51', '5', '2000-11-07', '2012-12-31'),
('61', '6', '2001-04-23', '2007-02-28'),
('62', '6', '2015-01-01', NULL);

INSERT INTO symptoms VALUES
('1', '11', '22', '2010-07-07', 'cough'),
('1', '12', '12', '2016-10-01', 'sore throat'),
('2', '21', '11', '2014-01-01', 'rash'),
('3', '31', '21', '2016-10-11', 'headache'),
('3', '31', '21', '2016-10-12', 'fatigue'),
('5', '51', '12', '2005-05-19', 'back pain'),
('6', '61', '11', '2002-08-17', 'back pain');

INSERT INTO diagnoses VALUES
('1', '12', '11', '2016-01-28', 'flu'),
('2', '21', '12', '2014-02-22', 'cold'),
('4', '41', '11', '2015-06-01', 'cancer'),
('5', '51', '12', '2006-01-01', 'ebola'),
('6', '62', '12', '2015-08-26', 'aids');

INSERT INTO drugs VALUES
('niacin', 'supplement'),
('420', 'painkiller'),
('tylenol', 'anti-inflammation'),
('vitamin x', 'supplement'),
('oxycotton', 'painkiller');

INSERT INTO dosage VALUES
('niacin', 'kid', 10),
('niacin', 'adult', 20),
('niacin', 'elder', 15),
('420', 'kid', 2),
('420', 'adult', 25),
('420', 'elder', 2),
('tylenol', 'kid', 7),
('tylenol', 'adult', 14),
('tylenol', 'elder', 21),
('vitamin x', 'kid', 45),
('vitamin x', 'adult', 90),
('vitamin x', 'elder', 85),
('oxycotton', 'kid', 1),
('oxycotton', 'adult', 2),
('oxycotton', 'elder', 1);

INSERT INTO medications VALUES
('1', '12', '11', '2016-05-27', '2016-06-01', '2016-08-08', 8, 'niacin'),
('2', '21', '12', '2014-06-06', '2014-06-07', '2014-12-02', 2, '420'),
('3', '31', '11', '2016-17-12', '2016-17-13', '2016-17-19', 9, 'tylenol'),
('4', '41', '12', '2016-06-03', '2016-08-01', '2016-08-30', 77, 'vitamin x'),
('5', '51', '11', '2011-04-20', '2011-04-21', '2011-05-01', 1, 'oxycotton');

INSERT INTO reportedallergies VALUES
('1', 'niacin'),
('3', 'oxycotton'),
('4', '420');

INSERT INTO inferredallergies VALUES
('tylenol', 'oxycotton'),
('oxycotton', 'tylenol'),
('niacin', 'vitamin x'),
('vitamin x', 'niacin');




