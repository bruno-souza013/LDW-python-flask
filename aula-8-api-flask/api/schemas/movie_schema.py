from api import ma

#importdando Schema e Fields
from marshmallow import Schema, fields

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("_id", "title", "description", "year")
        
        #tipando os dados
    _id = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    year = fields.Int(required=True)
        