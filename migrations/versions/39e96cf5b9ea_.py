"""empty message

Revision ID: 39e96cf5b9ea
Revises: 
Create Date: 2022-08-02 00:43:05.068250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39e96cf5b9ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doctor_name', sa.String(length=160), nullable=True),
    sa.Column('time', sa.String(length=60), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('doctor_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('specialty', sa.String(length=80), nullable=True),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('phoneNumber', sa.String(length=80), nullable=True),
    sa.Column('emailAddress', sa.String(length=160), nullable=True),
    sa.Column('companyName', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('emailAddress')
    )
    op.create_table('patient_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('DOB', sa.DateTime(), nullable=True),
    sa.Column('emailAddress', sa.String(length=160), nullable=True),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('time', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('booked', sa.Boolean(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('patient_profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.id'], ),
    sa.ForeignKeyConstraint(['patient_profile_id'], ['patient_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_list',
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('pat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doc_id'], ['doctor_profiles.id'], ),
    sa.ForeignKeyConstraint(['pat_id'], ['patient_profiles.id'], ),
    sa.PrimaryKeyConstraint('doc_id', 'pat_id')
    )
    op.create_table('patient_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_illness', sa.String(length=160), nullable=True),
    sa.Column('medication', sa.String(length=255), nullable=True),
    sa.Column('patient_profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_profile_id'], ['patient_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('blood_pressure', sa.String(length=255), nullable=True),
    sa.Column('blood_sugar', sa.String(length=255), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('patient_record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_record_id'], ['patient_record.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_of_complaints', sa.JSON(), nullable=True),
    sa.Column('patient_history_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_history_id'], ['patient_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('doctor_diagnosis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('history_id', sa.Integer(), nullable=True),
    sa.Column('doc_id', sa.Integer(), nullable=True),
    sa.Column('diagnosis', sa.String(length=255), nullable=True),
    sa.Column('prescription', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['doc_id'], ['doctor_profiles.id'], ),
    sa.ForeignKeyConstraint(['history_id'], ['patient_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('possible_causes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('possible_causes', sa.JSON(), nullable=True),
    sa.Column('patient_history_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_history_id'], ['patient_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('symptoms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_of_symptoms', sa.JSON(), nullable=True),
    sa.Column('patient_history_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_history_id'], ['patient_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('symptoms')
    op.drop_table('possible_causes')
    op.drop_table('doctor_diagnosis')
    op.drop_table('complaints')
    op.drop_table('patient_history')
    op.drop_table('patient_record')
    op.drop_table('patient_list')
    op.drop_table('appointments')
    op.drop_table('patient_profiles')
    op.drop_table('doctor_profiles')
    op.drop_table('appointment_schedule')
    # ### end Alembic commands ###