BEGIN;
  INSERT INTO account (acc_number, dollar_balance, branch_number)
  VALUES (447712, 300.00, (SELECT b.branch_number FROM branch b WHERE b.branch_name = "East Side Vancouver"))
COMMIT;
