def ref_field(model, field):
    for f in model._meta.fields:
        if f.get_attname() == field:
            return f
    return model._meta.get_field_by_name(field)
