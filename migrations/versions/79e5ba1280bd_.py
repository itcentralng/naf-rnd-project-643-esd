"""empty message

Revision ID: 79e5ba1280bd
Revises: d12506e69432
Create Date: 2024-04-04 01:14:50.174676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e5ba1280bd'
down_revision = 'd12506e69432'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehiclelog', schema=None) as batch_op:
        batch_op.create_foreign_key('foreignkey', 'vehicle', ['vehicle_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehiclelog', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###