import graphene as gp

name = gp.NonNull(gp.String)
appears_in = gp.List(gp.String)
appears_in_nn = gp.List(gp.NonNull(gp.String))
