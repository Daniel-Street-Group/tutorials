

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Estate Property module"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), 
                    ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    description = fields.Text()
    
    # Relations 
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=3)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        help='Cardinal direction of the garden')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max([offer for offer in property.offer_ids.mapped('price')], default=None)

    @api.onchange("garden")
    def _onchange_garden_area(self):
        self.garden_area = 10 if self.garden else None

    @api.onchange("garden")
    def _onchange_orientation(self):
        self.garden_orientation = 'north' if self.garden else None
    
    def action_set_cancelled(self):
        for property in self: 
            if property.state == 'sold':
                raise UserError("Sold properties cannot be cancelled")
            else: 
                property.state = 'cancelled'
        return True
            
    def action_set_sold(self):
        for property in self: 
            if property.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold")
            else:
                property.state = 'sold'
        return True


    
