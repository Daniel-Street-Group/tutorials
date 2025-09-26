

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    # Constraints
    _sql_constraints = [
        ('unique_name_constraint','unique(name)', 'Property types must be unique'),
    ]