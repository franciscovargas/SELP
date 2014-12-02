drop table if exists user;
create table user(
	id integer primary key autoincrement,
	user text not null,
	password text not null,
	postcode text not null
);
