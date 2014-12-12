drop table if exists user;
create table user(
	id integer primary key autoincrement,
	user text not null,
	password text not null,
	postcode text not null
);

drop table if exists edges;
create table edges(
	id integer primary key autoincrement,
	lat_start real not null,
	lat_end real not null,
	long_start real not null,
	long_end real not null,
	rank integer not null,
	user_id integer not null,
	foreign key(user_id) references user(id)
);

drop table if exists paths;
create table paths(
	id integer primary key autoincrement,
	path text not null,
	user_id integer not null,
	foreign key(user_id) references user(id)
);
