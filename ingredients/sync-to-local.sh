mysqldump -utest_user -pmypass -hec2-54-219-48-12.us-west-1.compute.amazonaws.com  prod  > bak.sql.tmp 

mysql -uroot -proot --database=prod < bak.sql.tmp

rm bak.sql.tmp
