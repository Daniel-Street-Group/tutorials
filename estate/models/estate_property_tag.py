

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"

    name = fields.Char(required=True)

    # Constraints
    _sql_constraints = [
        ('unique_name_constraint', 'unique(name)', 'Property tags must be unique'),
    ]