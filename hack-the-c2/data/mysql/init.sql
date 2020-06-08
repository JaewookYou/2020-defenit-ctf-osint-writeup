
create database defenit_ctf_2020;
use defenit_ctf_2020;
create table secret(ki11c0d3 varchar(255) not null, primary key(ki11c0d3));
insert into secret values("k1ll_th3_ALL_b4d_aR4n9_ransomeware");

create user 'b4d_aR4n9'@'172.22.0.3';
grant select on defenit_ctf_2020.secret to 'b4d_aR4n9'@'172.22.0.3';
flush privileges;
