# from graphene import String, Int, Float, Boolean, ID
import graphene as gp


street = gp.String(
    name="naoEhNome",
    description="Nome do ...",
    required=True,
    deprecation_reason="Inutilizado devido ...",
    default_value="Anonymous",
)
number = gp.Int()
lat = gp.Float()
urban_area = gp.Boolean()
last_update_date = gp.Date()
last_update_hour = gp.Time()
registration_date = gp.DateTime()
datas = gp.JSONString()

other = gp.Field(gp.String)
