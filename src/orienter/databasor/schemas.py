from marshmallow_sqlalchemy import SQLAlchemySchema, ModelConversionError, SQLAlchemyAutoSchema, auto_field

from . import models


class SectionSchema(SQLAlchemySchema):
    class Meta:
        model = models.Section
        load_instance = True

    id = auto_field("section_id")
    nazov = auto_field("name")


def setup_schema(Base, session):
    # Create a function which incorporates the Base and session information
    def setup_schema_fn():
        for class_ in Base._decl_class_registry.values():
            if hasattr(class_, "__tablename__"):
                if class_.__name__.endswith("Schema"):
                    raise ModelConversionError(
                        "For safety, setup_schema can not be used when a"
                        "Model class ends with 'Schema'"
                    )

                class Meta(object):
                    model = class_
                    sqla_session = session

                schema_class_name = "%sSchema" % class_.__name__

                schema_class = type(
                    schema_class_name, (SQLAlchemyAutoSchema,), {"Meta": Meta}
                )

                setattr(class_, "__marshmallow__", schema_class)

    return setup_schema_fn
