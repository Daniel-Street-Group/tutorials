

from odoo import api, fields, models

from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a property"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Offerer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    # Constrains 
    _sql_constraints = [
        ('price_constraint', 'CHECK(price > 0)', 'Price must be strictly positive'),
    ]


    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self: 
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Datetime.now() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self: 
            offer.validity = (offer.date_deadline - offer.create_date.date()).days
    
    def action_accept(self):
        for offer in self: 
            if (offer.property_id.buyer_id.name == False) and (offer.property_id.selling_price == 0.0): 
                print("SETTING VALUES")
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
        return True
    
    def action_refuse(self):
        for offer in self: 
            offer.status = 'refused'
        return True

