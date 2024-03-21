-- 8. Optimize simple search: Creates an index idx_name_first on the table names and the first letter of name.

ALTER TABLE names;
ADD COLUMN first_letter CHAR(1);

UPDATE names SET first_letter = (SUBSTRING(name, 1, 1));

CREATE INDEX idx_name_first ON names(first_letter);
