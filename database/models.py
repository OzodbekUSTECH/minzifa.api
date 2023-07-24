from database.db import metadata
import sqlalchemy

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), index=True),
    sqlalchemy.Column("office_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("offices.id"), index=True),
    sqlalchemy.Column("department_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("departments.id"), index=True),
    sqlalchemy.Column("manager_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("managers.id"), index=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("position", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),  
)


companies = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("SFM", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String)
)

office = sqlalchemy.Table(
    "offices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), index=True),
)


departments = sqlalchemy.Table(
    "departments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("office_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("offices.id"), index=True),
)

managers = sqlalchemy.Table(
    "managers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("SFM", sqlalchemy.String),
    sqlalchemy.Column("position", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("statys", sqlalchemy.Boolean),
    sqlalchemy.Column("department_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("departments.id"), index=True),
)



tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("department_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("departments.id"), index=True),
    sqlalchemy.Column("assigned_to", sqlalchemy.Integer),
)