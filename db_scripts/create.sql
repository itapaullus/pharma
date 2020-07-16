create sequence seq_pharma_id minvalue 1;

create table network (
    id int primary key default nextval('seq_pharma_id'),
    label varchar
);

create table distributor (
    id int primary key default nextval('seq_pharma_id'),
    label varchar
);

create table manager (
    id int primary key default nextval('seq_pharma_id'),
    label varchar
);

create table client (
    id int primary key default nextval('seq_pharma_id'),
    label varchar,
    taxid varchar,
    network_id int references network(id)
);

create table region (
    id int primary key default nextval('seq_pharma_id'),
    label varchar unique
);

create table region_synonyms (
    id int primary key default nextval('seq_pharma_id'),
    region_id int references region(id),
    synonym varchar
);

create table manager2network (
    id int primary key default nextval('seq_pharma_id'),
    manager_id int references manager(id),
    network_id int references network(id),
    link_date date,
    status    bool
);

create table manager2client (
    id int primary key default nextval('seq_pharma_id'),
    manager_id  int references manager(id),
    client_id   int references client(id),
    link_date   date,
    status      bool
);

create table branch (
    id int primary key default nextval('seq_pharma_id'),
    label varchar,
    region_id   int references region(id),
    distributor_id  int references distributor(id)
);